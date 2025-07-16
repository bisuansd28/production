from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def get_user_or_ip():
    return request.form.get("id") or get_remote_address()

db = SQLAlchemy()
login_manager = LoginManager()
limiter = Limiter(key_func=get_user_or_ip)