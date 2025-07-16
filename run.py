from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    db.create_all()
    from app.models.models import User
    from werkzeug.security import generate_password_hash
    if not User.query.first():
        db.session.add(User(id="taiyo", name="taiyo", pw=generate_password_hash("taiyo")))
        db.session.commit()

if __name__ == "__main__":
    # print(app.url_map)
    app.run(debug=True)