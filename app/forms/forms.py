from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SubmitField, DateTimeLocalField, TextAreaField, BooleanField, MultipleFileField
from wtforms.validators import DataRequired
from datetime import datetime

# WTFクラス
class PostForm(FlaskForm):
    title = StringField("タイトル", validators=[DataRequired("タイトルは必須です")])
    content = TextAreaField("内容", validators=[DataRequired("投稿内容は必須です")])
    media = RadioField("画像・動画", choices=[("none", "なし"), ("upload", "画像・動画"), ("youtube", "YouTube")], default="none", validators=[DataRequired()])
    file = MultipleFileField("アップロード")
    youtube = StringField("URL")
    tags = StringField("タグ(,区切り)")
    date = DateTimeLocalField("日時", format="%Y-%m-%dT%H:%M", default=datetime.now)
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
    media = RadioField("画像・動画", choices=[("none", "なし"), ("upload", "画像・動画"), ("youtube", "YouTube")], default="none", validators=[DataRequired()])
    file = MultipleFileField("アップロード")
    youtube = StringField("URL")
    tags = StringField("タグ(,区切り)")
    date = DateTimeLocalField("日時", format="%Y-%m-%dT%H:%M")
    submit = SubmitField("投稿")

class ConcertForm(FlaskForm):
    title = StringField("タイトル", validators=[DataRequired("タイトルは必須です")])
    text = TextAreaField("テキスト")
    images = MultipleFileField("画像")
    submit = SubmitField("追加")

class EditConcert(FlaskForm):
    title = StringField("タイトル", validators=[DataRequired("タイトルは必須です")])
    text = TextAreaField("テキスト")
    images = MultipleFileField("画像")
    top = BooleanField("トップページ")
    submit = SubmitField("編集")