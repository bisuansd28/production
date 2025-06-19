from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_paginate import Pagination, get_page_parameter
from app.models.models import Post, User, Log, Tag, Concert, ConcertImage, PostImage, Counter
from app.extensions import db, login_manager
from app.forms.forms import *
from datetime import datetime, date, timedelta
import os
from werkzeug.security import generate_password_hash, check_password_hash
import json
import markdown
import re

# blueprintの作成
main_bp = Blueprint("main", __name__)
# ログインマネージャー
login_manager.login_view = "main.login"
# ファイルアップロード
upload_folder = "app/static/uploads"

def convert_youtube_url_to_embed(url):
    match = re.search(r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^\s&]+)", url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}"
    match = re.search(r"(?:https?://)?youtu\.be/([^\s?&]+)", url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}"
    print("error")
    return None

@main_bp.route("/")
def index():
    session.permanent = True
    today = date.today()
    daily = Counter.query.filter_by(date=today).first()
    last_count = Counter.query.order_by(Counter.date.desc()).first()
    user_count = last_count.user_count if last_count else 0
    if not daily:
        daily = Counter(date=today, access_count=0, user_count=user_count)
        db.session.add(daily)
        db.session.commit()

    now = datetime.now()
    last_visit = session.get("last_visit")
    if not last_visit:
        daily.user_count += 1
        daily.access_count += 1
        session["last_visit"] = now.isoformat()
    else:
        last_visit_time = datetime.fromisoformat(last_visit)
        if now - last_visit_time > timedelta(hours=1):
            daily.access_count += 1
            session["last_visit"] = now.isoformat()
    db.session.commit()

    posts = Post.query.order_by(Post.date.desc()).limit(5).all()
    concert = Concert.query.filter_by(top=True).first()
    for post in posts:
        post.date_str = f"{post.date.year}年{post.date.month}月{post.date.day}日"
    return render_template("index.html", posts=posts, concert=concert)

@main_bp.route("/news")
def news():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = 10
    all_posts = Post.query.order_by(Post.date.desc()).all()
    for post in all_posts:
        post.date_str = f"{post.date.year}年{post.date.month}月{post.date.day}日"
    total = len(all_posts)
    posts = all_posts[(page - 1) * per_page: page * per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework="boostrap5")
    return render_template("news.html", posts=posts, pagination=pagination)

@main_bp.route("/news/<int:id>")
def article(id):
    article = Post.query.get_or_404(id)
    article.view_count += 1
    db.session.commit()
    article.text = markdown.markdown(article.content, extensions=['nl2br'])
    print(article.text)
    article.date_str = f"{article.date.year}年{article.date.month}月{article.date.day}日"
    return render_template("article.html", article=article)

@main_bp.route("/concert")
def concerts():
    concerts = Concert.query.order_by(Concert.id.desc()).all()
    return render_template("concerts.html", concerts=concerts)

@main_bp.route("/concert/<int:id>")
def concert(id):
    concert = Concert.query.get(id)
    concert.view_count += 1
    db.session.commit()
    concert.text = markdown.markdown(concert.text, extensions=['nl2br'])
    return render_template("concert.html", concert=concert)

@main_bp.route("/joinus")
def join_us():
    return render_template("joinus.html")

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
    count = Counter.query.order_by(Counter.date.desc()).first()
    return render_template("admin.html", count=count)

@main_bp.route("/admin/login", methods=["GET", "POST"])
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

@main_bp.route("/admin/logout")
@login_required
def logout():
    new_log = Log(user_id=str(current_user.id), 
                  action_type="logout")
    logout_user()
    db.session.add(new_log)
    db.session.commit()
    return redirect(url_for("main.login"))

@main_bp.route("/admin/user")
@login_required
def user():
    users = User.query.all()
    return render_template("user_list.html", users=users)

@main_bp.route("/admin/post")
@login_required
def post():
    posts = Post.query.all()
    return render_template("post_list.html", posts=posts)

@main_bp.route("/admin/concert")
@login_required
def concert_list():
    concerts = Concert.query.all()
    return render_template("concert_list.html", concerts=concerts)

@main_bp.route("/admin/user/create", methods=["GET", "POST"])
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

@main_bp.route("/admin/user/edit/<string:id>", methods=["GET", "POST"])
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

@main_bp.route("/admin/user/delete/<string:id>")
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

@main_bp.route("/admin/post/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        media = form.media.data
        date = form.date.data
        if media == "youtube":
            url = convert_youtube_url_to_embed(form.youtube.data)
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
        new_post = Post(title=title, content=content, media=media, url=url, tags=tags, date=date)
        db.session.add(new_post)
        db.session.commit()

        for file in form.file.data:
            if file:
                filename = datetime.now().strftime("%Y%m%d%H%M%S" + os.path.splitext(file.filename)[1])
                os.makedirs(upload_folder, exist_ok=True)
                file.save(os.path.join(upload_folder, filename))
                image = PostImage(post_id=new_post.id, path=filename)
                db.session.add(image)

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

@main_bp.route("/admin/post/edit/<int:id>", methods=["GET", "POST"])
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
        post.date = form.date.data
        if post.media == "youtube":
            post.url = convert_youtube_url_to_embed(form.youtube.data)
        else:
            post.url = None
        tag_names = [t.strip() for t in form.tags.data.split(",") if t.strip()]
        print(form.tags.data)
        tags = []
        for name in tag_names:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
                db.session.add(tag)
            tags.append(tag)
        post.tags = tags
        db.session.commit()

        for file in form.file.data:
            if file:
                filename = datetime.now().strftime("%Y%m%d%H%M%S" + os.path.splitext(file.filename)[1])
                os.makedirs(upload_folder, exist_ok=True)
                file.save(os.path.join(upload_folder, filename))
                image = PostImage(post_id=post.id, path=filename)
                db.session.add(image)

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
        if post.media == "youtube" and post.url:
            form.youtube.data = post.url
    return render_template("edit_post.html", form=form)

@main_bp.route("/admin/post/delete/<int:id>")
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

@main_bp.route('/admin/concert/create', methods=['GET', 'POST'])
def create_concert():
    form = ConcertForm()
    if form.validate_on_submit():
        concert = Concert(title=form.title.data, text=form.text.data)
        db.session.add(concert)
        db.session.commit()
        for file in form.images.data:
            if file:
                filename = datetime.now().strftime("%Y%m%d%H%M%S" + os.path.splitext(file.filename)[1])
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                image = ConcertImage(concert_id=concert.id, path=filename)
                db.session.add(image)
        new_log = Log(user_id=str(current_user.id), 
            action_type="create_concert", 
            target_table="concerts", 
            target_id=concert.id, 
            text=json.dumps({
                "title" : concert.title, 
                "text" : concert.text
                        }, )
        )
        db.session.add(new_log)
        db.session.commit()
        return redirect(url_for('main.concert_list'))
    return render_template('create_concert.html', form=form)

@main_bp.route("/admin/concert/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_concert(id):
    concert = Concert.query.get_or_404(id)
    form = EditConcert(obj=concert)
    if form.validate_on_submit():
        old_title = concert.title
        old_text = concert.text
        concert.title = form.title.data
        concert.text = form.text.data
        for file in form.images.data:
            if file:
                filename = datetime.now().strftime("%Y%m%d%H%M%S" + os.path.splitext(file.filename)[1])
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)
                image = ConcertImage(concert_id=concert.id, path=filename)
                db.session.add(image)
        db.session.commit()
        new_log = Log(user_id=str(current_user.id), 
                      action_type="edit_concert", 
                      target_table="concerts", 
                      target_id=concert.id, 
                      text=json.dumps({
                          "old_title" : old_title, 
                          "new_title" : concert.title, 
                          "old_text" : old_text, 
                          "new_text" : concert.text
                        }, 
                        ensure_ascii=False))
        db.session.add(new_log)
        db.session.commit()
        flash("編集完了")
        return redirect(url_for("main.concert_list"))
    return render_template("edit_concert.html", form=form)

@main_bp.route("/admin/concert/delete/<int:id>")
@login_required
def delete_concert(id):
    concert = Concert.query.get_or_404(id)
    new_log = Log(user_id=str(current_user.id), 
                action_type="delete_concert", 
                target_table="concerts", 
                target_id=concert.id, 
                text=json.dumps({
                    "title" : concert.title, 
                    "text" : concert.text
                    }, 
                    ensure_ascii=False))
    db.session.delete(concert)
    db.session.add(new_log)
    db.session.commit()
    flash("投稿削除完了")
    return redirect(url_for("main.concert_list"))