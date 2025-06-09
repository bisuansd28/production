from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_paginate import Pagination, get_page_parameter
from app.models.models import Post, User, Log, Tag
from app.extensions import db, login_manager
from app.forms.forms import *
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
import json

# blueprintの作成
main_bp = Blueprint("main", __name__)
# ログインマネージャー
login_manager.login_view = "main.login"
# ファイルアップロード
upload_folder = "app/static/uploads"

@main_bp.route("/")
def index():
    posts = Post.query.order_by(Post.date.desc()).limit(5).all()
    for post in posts:
        post.date_str = f"{post.date.year}年{post.date.month}月{post.date.day}日"
    return render_template("index.html", posts=posts)

@main_bp.route("/news")
def news():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 2
    all_posts = Post.query.order_by(Post.date.desc()).all()
    for post in all_posts:
        post.date_str = f"{post.date.year}年{post.date.month}月{post.date.day}日"
    total = len(all_posts)
    posts = all_posts[(page - 1) * per_page: page * per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework="boostrap5")
    return render_template("news.html", posts=posts, pagination=pagination)

@main_bp.route("/news/<int:id>")
def article(id):
    post = Post.query.get_or_404(id)
    return render_template("article.html", post=post)

# 後で消す開発用
@main_bp.route("/dev")
def dev():
    id = "taiyo"
    user = User.query.filter_by(id=id).first()
    login_user(user)
    return render_template("admin.html")

@main_bp.route("/admin")
@login_required
def admin():
    return render_template("admin.html")

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        id = form.id.data
        pw = form.id.data
        user = User.query.filter_by(id=id).first()
        if user and check_password_hash(user.pw, pw):
            login_user(user)
            new_log = Log(user_id=str(current_user.id), 
                          action_type="login")
            db.session.add(new_log)
            db.session.commit()
            return redirect(url_for("main.admin"))
        flash("idまたはpwが間違っています")
    return render_template("login.html", form=form)

@main_bp.route("/logout")
@login_required
def logout():
    new_log = Log(user_id=str(current_user.id), 
                  action_type="logout")
    logout_user()
    db.session.add(new_log)
    db.session.commit()
    return redirect(url_for("main.login"))

@main_bp.route("/user")
@login_required
def user():
    users = User.query.all()
    return render_template("user_list.html", users=users)

@main_bp.route("/post")
@login_required
def post():
    posts = Post.query.all()
    return render_template("post_list.html", posts=posts)

@main_bp.route("/user/create", methods=["GET", "POST"])
@login_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        id = form.id.data
        name = form.name.data
        pw = form.pw.data
        hashed_pw = generate_password_hash(pw)
        new_user = User(id=id, name=name, pw=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        new_log = Log(user_id=str(current_user.id), 
                      action_type="create_user", 
                      target_table="users", 
                      target_id=new_user.id)
        db.session.add(new_log)
        db.session.commit()
        flash("ユーザー登録完了")
        return redirect(url_for("main.user"))
    return render_template("create_user.html", form=form)

@main_bp.route("/user/edit/<string:id>", methods=["GET", "POST"])
@login_required
def edit_user(id):
    user = User.query.get_or_404(id)
    form = EditUser(obj=user)
    form.pw.data = ""
    if form.validate_on_submit():
        old_id = user.id
        old_name = user.name
        old_pw = user.pw
        user.id = form.id.data
        user.name = form.name.data
        if form.pw.data:
            user.pw = generate_password_hash(form.pw.data)
        db.session.commit()
        new_log = Log(user_id=str(current_user.id), 
                      action_type="edit_user", 
                      target_table="users", 
                      target_id=old_id, 
                      text=json.dumps({
                          "old_id" : old_id, 
                          "new_id" : user.id, 
                          "old_name" : old_name, 
                          "new_name" : user.name, 
                          "old_pw" : old_pw, 
                          "new_pw" : user.pw
                        }, 
                        ensure_ascii=False))
        db.session.add(new_log)
        db.session.commit()
        flash("ユーザー情報編集完了")
        return redirect(url_for("main.user"))
    return render_template("edit_user.html", form=form)

@main_bp.route("/user/delete/<string:id>")
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash("自分自身は削除できません。")
        return redirect(url_for("main.user"))
    new_log = Log(user_id=str(current_user.id), 
                  action_type="delete_user", 
                  target_table="users", 
                  target_id=user.id)
    db.session.delete(user)
    db.session.add(new_log)
    db.session.commit()
    flash("ユーザー削除完了")
    return redirect(url_for("main.user"))

@main_bp.route("/post/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        media = form.media.data
        if media == "upload":
            filename = datetime.now().strftime("%Y%m%d%H%M%S" + os.path.splitext(form.file.data.filename)[1])
            os.makedirs(upload_folder, exist_ok=True)
            form.file.data.save(os.path.join(upload_folder, filename))
            url = f"/static/uploads/{filename}"
        elif media == "youtube":
            url = form.youtube.data
        else:
            url = None
        tag_names = [t.strip() for t in form.tags.data.split(",") if t.strip()]
        tags = []
        for name in tag_names:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
                db.session.add(tag)
            tags.append(tag)
        
        new_post = Post(title=title, content=content, media=media, url=url, tags=tags)
        db.session.add(new_post)
        db.session.commit()
        new_log = Log(user_id=str(current_user.id), 
                      action_type="create_post", 
                      target_table="Post", 
                      target_id=new_post.id, 
                      text=json.dumps({"title" : title, 
                                       "content" : content, 
                                       "media" : media, 
                                       "url" : url, 
                                       "tag" : [tag.name for tag in tags]
                                       }, 
                                       ensure_ascii=False))
        db.session.add(new_log)
        db.session.commit()
        flash("投稿完了")
        return redirect(url_for("main.post"))
    return render_template("create_post.html", form=form)

@main_bp.route("/post/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_post(id):
    post = Post.query.get_or_404(id)
    form = EditPost(obj=post)
    if form.validate_on_submit():
        old_title = post.title
        old_content = post.content
        old_media = post.media
        old_url = post.url
        old_date = post.date
        old_tags = post.tags
        post.title = form.title.data
        post.content = form.content.data
        post.media = form.media.data
        if post.media == "upload":
            filename = datetime.now().strftime("%Y%m%d%H%M%S" + os.path.splitext(form.file.data.filename)[1])
            os.makedirs(upload_folder, exist_ok=True)
            form.file.data.save(os.path.join(upload_folder, filename))
            post.url = f"/static/uploads/{filename}"
        elif post.media == "youtube":
            post.url = form.youtube.data
        else:
            post.url = None
        tag_names = [t.strip() for t in form.tags.data.split(",") if t.strip()]
        print(form.tags.data)
        tags = []
        for name in tag_names:
            tag = Tag.query.filter_by(name=name).first()
            print("2")
            if not tag:
                print("a")
                tag = Tag(name=name)
                db.session.add(tag)
            tags.append(tag)
        post.tags = tags
        db.session.commit()
        new_log = Log(user_id=str(current_user.id), 
                      action_type="edit_post", 
                      target_table="posts", 
                      target_id=post.id, 
                      text=json.dumps({
                          "old_title" : old_title, 
                          "new_title" : post.title, 
                          "old_content" : old_content, 
                          "new_content" : post.content, 
                          "old_media" : old_media, 
                          "new_media" : post.media, 
                          "old_url" : old_url, 
                          "new_url" : post.url, 
                          "old_tags" : [tag.name for tag in old_tags], 
                          "new_tags" : [tag.name for tag in post.tags], 
                          "old_date" : old_date.isoformat(), 
                          "new_date" : post.date.isoformat()
                        }, 
                        ensure_ascii=False))
        db.session.add(new_log)
        db.session.commit()
        flash("編集完了")
        return redirect(url_for("main.post"))
    else:
        form.tags.data = ", ".join(tag.name for tag in post.tags)
    return render_template("edit_post.html", form=form)

@main_bp.route("/post/delete/<int:id>")
@login_required
def delete_post(id):
    post = Post.query.get_or_404(id)
    new_log = Log(user_id=str(current_user.id), 
                action_type="delete_post", 
                target_table="posts", 
                target_id=post.id, 
                text=json.dumps({
                    "title" : post.title, 
                    "content" : post.content, 
                    "media" : post.media, 
                    "url" : post.url
                    }, 
                    ensure_ascii=False))
    db.session.delete(post)
    db.session.add(new_log)
    db.session.commit()
    flash("投稿削除完了")
    return redirect(url_for("main.post"))