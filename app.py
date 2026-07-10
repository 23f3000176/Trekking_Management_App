from flask import Flask
from config import (
    SECRET_KEY,
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS,
)
from extensions import db

app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)


import models

with app.app_context():
    db.create_all()

    admin=models.User.query.filter_by(username="admin").first()
    if not admin:
        admin = models.User(
            username="admin",
            password="admin123",
            name="Admin User",
            role="admin",
        )
        db.session.add(admin)
        db.session.commit()

from routes import main




app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)