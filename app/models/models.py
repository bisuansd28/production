from app.extensions import db
from datetime import datetime
from flask_login import UserMixin

post_tags = db.Table("post_tags", 
                     db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True), 
                     db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True)
                     )

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    media = db.Column(db.String(10))
    url = db.Column(db.String(100))
    tags = db.relationship("Tag", secondary=post_tags, back_populates="posts")

class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    posts = db.relationship("Post", secondary=post_tags, back_populates="tags")


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    pw = db.Column(db.String(100), nullable=False)

class Log(db.Model):
    __tablename__ = "logs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(20), db.ForeignKey("users.id", onupdate="CASCADE"), nullable=False)
    action_type = db.Column(db.String(20), nullable=False)
    target_table = db.Column(db.String(10))
    target_id = db.Column(db.String(10))
    text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    
    