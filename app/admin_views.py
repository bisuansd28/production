from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView
from flask_login import current_user
from flask import redirect, url_for
from wtforms import StringField, RadioField
from app.models.models import Concert
from app.extensions import db
from flask_admin.form import FileUploadField
import os

class MyAdminIndexView(AdminIndexView):
    def __init__(self, **kwargs):
        super().__init__(url='/management', **kwargs)
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == "taiyo"
    def inaccessible_callback(self, name, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for("main.admin"))
        else:
            return redirect(url_for('main.login'))

class PostView(ModelView):
    column_list = ["id", "title", "content", "media", "url", "tags", "date", "view_count"]
    form_columns = ["title", "content", "media", "url", "tags", "date"]
    column_default_sort = ("id", True)

    form_overrides = {
        'media': RadioField,
    }
    form_args = {
        'media': {
            'choices': [
                ('none', 'なし'),
                ('upload', '画像・動画'),
                ('youtube', 'youtube'),
            ], 
            'default': "none"
        }
    }
    form_widget_args = {
    'media': {
        'class': 'form-check-input'
    }
    }
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == "taiyo"
    
class PostImageView(ModelView):
    column_list = ["id", "post_id", "path"]
    column_default_sort = ("id", True)
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == "taiyo"

class UserView(ModelView):
    column_list = ["id", "name", "pw"]
    form_columns = ["id", "name", "pw"]
    column_default_sort = ("id", False)
    can_delete = False
    can_create = False
    can_edit = False
    form_extra_fields = {
        "id": StringField("User ID")
    }
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == "taiyo"
    
class TagView(ModelView):
    column_list = ["id", "name", "post"]
    can_create = False
    column_default_sort = ("id", False)
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == "taiyo"
    
class LogView(ModelView):
    column_list = ["id", "user_id", "action_type", "target_table", "target_id", "text", "timestamp"]
    can_create = False
    column_default_sort = ("id", True)
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == "taiyo"
    
class ConcertView(ModelView):
    column_list = ["id", "url", "title", "text", "top", "image", "end", "view_count"]
    column_default_sort = ("id", True)
    form_columns = ["title", "text", "top", "image"]
    form_args = {
        'top': {
            'default': False
        }
    }
    form_extra_fields = {
        'image': FileUploadField('Image',
            base_path=os.path.join(os.path.dirname(__file__), 'static/uploads'),
            relative_path='')
    }
    def on_model_change(self, form, model, is_created):
       if model.top:
           Concert.query.filter(Concert.id != model.id, Concert.top == True).update({"top": False})
           db.session.commit()
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == "taiyo"
    
class ConcertImageView(ModelView):
    column_list = ["id", "concert_id", "path"]
    column_default_sort = ("id", True)
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == "taiyo"
    
class CounterView(ModelView):
    column_list = ["id", "date", "access_count", "user_count", "date"]
    column_default_sort = ("id", True)
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == "taiyo"

class NoteView(ModelView):
    column_list = ["id", "title", "content", "media", "url", "tags", "date", "view_count"]
    form_columns = ["title", "content", "media", "url", "tags", "date"]
    column_default_sort = ("id", True)

    form_overrides = {
        'media': RadioField,
    }
    form_args = {
        'media': {
            'choices': [
                ('none', 'なし'),
                ('upload', '画像・動画'),
                ('youtube', 'youtube'),
            ], 
            'default': "none"
        }
    }
    form_widget_args = {
    'media': {
        'class': 'form-check-input'
    }
    }
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == "taiyo"

class NoteImageView(ModelView):
    column_list = ["id", "note_id", "path"]
    column_default_sort = ("id", True)
    def is_accessible(self):
        return current_user.is_authenticated and current_user.id == "taiyo"