from app.extensions import db
from datetime import date
from flask_login import UserMixin

post_tags = db.Table("post_tags", 
                     db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True), 
                     db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True)
                     )
note_tags = db.Table("note_tags", 
                     db.Column("note_id", db.Integer, db.ForeignKey("note.id"), primary_key=True), 
                     db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True)
                     )

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, default=date.today, nullable=False)
    media = db.Column(db.String(16))
    url = db.Column(db.String(255))
    images = db.relationship("PostImage", backref="post", cascade="all, delete-orphan")
    tags = db.relationship("Tag", secondary=post_tags, back_populates="posts")
    view_count = db.Column(db.Integer, default=0, nullable=False)

class PostImage(db.Model):
    __tablename__ = "post_images"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    path = db.Column(db.String(255))

class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), unique=True, nullable=False)
    posts = db.relationship("Post", secondary=post_tags, back_populates="tags")
    note = db.relationship("Note", secondary=note_tags, back_populates="tags")
    def __str__(self):
        return self.name

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.String(16), primary_key=True, nullable=False)
    name = db.Column(db.String(16), nullable=False)
    pw = db.Column(db.String(256), nullable=False)
    def __str__(self):
        return self.name

class Log(db.Model):
    __tablename__ = "logs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(16), db.ForeignKey("users.id", onupdate="CASCADE"), nullable=False)
    action_type = db.Column(db.String(32), nullable=False)
    target_table = db.Column(db.String(16))
    target_id = db.Column(db.String(16))
    text = db.Column(db.Text)
    timestamp = db.Column(db.Date, default=date.today)
    
class Concert(db.Model):
    __tablename__ = "concerts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), nullable=False)
    text = db.Column(db.Text)
    top = db.Column(db.Boolean, default=False)
    end = db.Column(db.Boolean, default=False)
    date = db.Column(db.Date, default=date.today, nullable=False)
    url = db.Column(db.String(32), unique=True, nullable=False)
    images = db.relationship("ConcertImage", backref="concert", cascade="all, delete-orphan")
    view_count = db.Column(db.Integer, default=0, nullable=False)

class ConcertImage(db.Model):
    __tablename__ = "concert_images"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    concert_id = db.Column(db.Integer, db.ForeignKey("concerts.id"))
    path = db.Column(db.String(255))

class Counter(db.Model):
    __tablename__ = "counter"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    access_count = db.Column(db.Integer, default=0)
    user_count = db.Column(db.Integer)

class Note(db.Model):
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, default=date.today, nullable=False)
    media = db.Column(db.String(16))
    url = db.Column(db.String(255))
    images = db.relationship("NoteImage", backref="note", cascade="all, delete-orphan")
    tags = db.relationship("Tag", secondary=note_tags, back_populates="note")
    view_count = db.Column(db.Integer, default=0, nullable=False)

class NoteImage(db.Model):
    __tablename__ = "note_images"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note_id = db.Column(db.Integer, db.ForeignKey("note.id"))
    path = db.Column(db.String(255))