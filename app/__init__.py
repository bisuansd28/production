from flask import Flask
from app.extensions import db, login_manager, limiter
from app.routes.routes import main_bp
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3
from datetime import timedelta

@event.listens_for(Engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
    db.init_app(app)

    limiter.init_app(app)

    from app.models import models

    # blueprintの登録
    # 登録しないとmain_bp内のルートやテンプレート、静的ファイルが使えない
    app.register_blueprint(main_bp)

    # wtf用
    app.config["SECRET_KEY"] = "8fe8576e1babe36dbcb59e2d27dc2309ac47ec609ec8c332b932623cc3502a6c"

    login_manager.init_app(app)
    from flask_admin import Admin
    from app.admin_views import MyAdminIndexView, PostView, TagView, UserView, LogView, ConcertView, ConcertImageView, NoteImageView, NoteView, PostImageView, CounterView
    admin = Admin(name='Admin', url='/management', template_mode='bootstrap3', index_view=MyAdminIndexView())
    admin.init_app(app)

    from app.models.models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    
    from app.models.models import Post, Tag, User, Log, Concert, ConcertImage, PostImage, Note, NoteImage, Counter
    
    admin.add_view(PostView(Post, db.session))
    admin.add_view(PostImageView(PostImage, db.session))
    admin.add_view(TagView(Tag, db.session))
    admin.add_view(UserView(User, db.session))
    admin.add_view(LogView(Log, db.session))
    admin.add_view(ConcertView(Concert, db.session))
    admin.add_view(ConcertImageView(ConcertImage, db.session))
    admin.add_view(NoteView(Note, db.session))
    admin.add_view(NoteImageView(NoteImage, db.session))
    admin.add_view(CounterView(Counter, db.session))

    app.permanent_session_lifetime = timedelta(days=9999)

    return app