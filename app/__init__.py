from flask import Flask
from app.extensions import db, login_manager
from app.routes.routes import main_bp
from app.models.models import User
from sqlalchemy import event
from sqlalchemy.engine import Engine
import sqlite3

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
    login_manager.init_app(app)

    from app.models import models

    # blueprintの登録
    # 登録しないとmain_bp内のルートやテンプレート、静的ファイルが使えない
    app.register_blueprint(main_bp)

    # wtf用
    app.config["SECRET_KEY"] = "f4fb392f440d1731b8c09a0b6f588559a03081b0cf705612008a04c4aaef89b5"

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    return app