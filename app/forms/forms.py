from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, DateTimeLocalField, TextAreaField, BooleanField, MultipleFileField, DateField
from wtforms.validators import DataRequired
from datetime import date

# WTFクラス
class PostForm(FlaskForm):
    title = StringField("タイトル", validators=[DataRequired("タイトルは必須です")])
    content = TextAreaField("内容", validators=[DataRequired("投稿内容は必須です")])
    media = RadioField("画像", choices=[("none", "なし"), ("upload", "画像"), ("youtube", "YouTube")], default="none", validators=[DataRequired()])
    file = MultipleFileField("アップロード")
    youtube = StringField("URL")
    tags = StringField("タグ(,区切り)")
    date = DateField("日付", format="%Y-%m-%d", default=date.today)
    submit = SubmitField("投稿")

class UserForm(FlaskForm):
    id = StringField("id", validators=[DataRequired("idは必須です")])
    name = StringField("名前", validators=[DataRequired("名前は必須です")])
    pw = StringField("password", validators=[DataRequired("passwordは必須です")])
    submit = SubmitField("追加")

class LoginForm(FlaskForm):
    id = StringField("id", validators=[DataRequired("idは必須です")])
    pw = StringField("password", validators=[DataRequired("passwordは必須です")])
    submit = SubmitField("ログイン")

class EditUser(FlaskForm):
    id = StringField("id", validators=[DataRequired("idは必須です")])
    name = StringField("名前", validators=[DataRequired("名前は必須です")])
    pw = StringField("password")
    submit = SubmitField("編集")

class EditPost(FlaskForm):
    title = StringField("タイトル", validators=[DataRequired("タイトルは必須です")])
    content = TextAreaField("内容", validators=[DataRequired("投稿内容は必須です")])
    media = RadioField("画像", choices=[("none", "なし"), ("upload", "画像"), ("youtube", "YouTube")], default="none", validators=[DataRequired()])
    file = MultipleFileField("アップロード")
    youtube = StringField("URL")
    tags = StringField("タグ(,区切り)")
    date = DateField("日付", format="%Y-%m-%d")
    submit = SubmitField("投稿")

class ConcertForm(FlaskForm):
    title = StringField("タイトル", validators=[DataRequired("タイトルは必須です")])
    text = TextAreaField("テキスト")
    url = StringField("URL", validators=[DataRequired("URLは必須です")])
    images = MultipleFileField("画像")
    date = DateField("日付", format="%Y-%m-%d")
    submit = SubmitField("追加")

class EditConcert(FlaskForm):
    title = StringField("タイトル", validators=[DataRequired("タイトルは必須です")])
    text = TextAreaField("テキスト")
    url = StringField("URL", validators=[DataRequired("URLは必須です")])
    images = MultipleFileField("画像")
    top = BooleanField("トップページ")
    end = BooleanField("終了")
    date = DateField("日付", format="%Y-%m-%d")
    submit = SubmitField("編集")

class NoteForm(FlaskForm):
    title = StringField("タイトル", validators=[DataRequired("タイトルは必須です")])
    content = TextAreaField("内容", validators=[DataRequired("投稿内容は必須です")])
    media = RadioField("画像", choices=[("none", "なし"), ("upload", "画像"), ("youtube", "YouTube")], default="none", validators=[DataRequired()])
    file = MultipleFileField("アップロード")
    youtube = StringField("URL")
    tags = StringField("タグ(,区切り)")
    date = DateField("日付", format="%Y-%m-%d", default=date.today)
    submit = SubmitField("投稿")

class EditNote(FlaskForm):
    title = StringField("タイトル", validators=[DataRequired("タイトルは必須です")])
    content = TextAreaField("内容", validators=[DataRequired("投稿内容は必須です")])
    media = RadioField("画像", choices=[("none", "なし"), ("upload", "画像"), ("youtube", "YouTube")], default="none", validators=[DataRequired()])
    file = MultipleFileField("アップロード")
    youtube = StringField("URL")
    tags = StringField("タグ(,区切り)")
    date = DateField("日付", format="%Y-%m-%d")
    submit = SubmitField("投稿")