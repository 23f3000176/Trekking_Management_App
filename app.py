from flask import Flask , render_template
from controller.database import db
from controller.config import config
from controller.models import User, Trek, Booking
 
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

with app.app_context():
    db.create_all()
    # Create default admin
    admin = User.query.filter_by(role="Admin").first()

    if not admin:
        admin = User(
            username="admin",
            email="admin@trek.com",
            name="Administrator",
            contact="9999999999",
            role="Admin",
            status="Approved"
        )

        admin.password = "admin123"

        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully!")

@app.route('/')
def index():
    return render_template('hello.html')
    

if __name__ == '__main__':
    app.run(debug=True)
