from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    db.create_all()
    from app.models.models import User, Post
    from werkzeug.security import generate_password_hash
    if not User.query.first():
        db.session.add(User(id="taiyo", name="taiyo", pw=generate_password_hash("taiyo")))
        db.session.add(Post(title="シマエナガと「夢の意味」を歌いませんか？", content="当団の第1回定期演奏会で演奏した上田真樹作曲『夢の意味』を練習いたします。参加者の皆さまと一緒に練習し、最後に演奏を行いたいと考えております。", media=None))
        db.session.add(Post(title="222シマエナガと「夢の意味」を歌いませんか？", content="222当団の第1回定期演奏会で演奏した上田真樹作曲『夢の意味』を練習いたします。参加者の皆さまと一緒に練習し、最後に演奏を行いたいと考えております。", media=None))
        db.session.commit()

if __name__ == "__main__":
    # print(app.url_map)
    app.run(debug=True)