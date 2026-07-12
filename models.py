from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    passhash = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    approved = db.Column(db.Boolean, default=False)
    
    bookings = db.relationship("Booking", backref="user", lazy=True)
    staff_profile = db.relationship(
        "StaffProfile",
        backref="user",
        uselist=False,
    )

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")
    @password.setter
    def password(self, password):
        self.passhash = generate_password_hash(password) 
    def check_password(self, password):
        return check_password_hash(self.passhash, password)


class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="open")
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    bookings = db.relationship("Booking", backref="trek", lazy=True)


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)

    trek_id = db.Column(db.Integer,db.ForeignKey("treks.id"),nullable=False)

    booking_date = db.Column(db.String(20), nullable=False)
    persons = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    booking_status = db.Column(db.String(20), nullable=False, default="pending")
    payment_status = db.Column(db.String(20), nullable=False, default="unpaid")


class StaffProfile(db.Model):
    __tablename__ = "staff_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )

    phone = db.Column(db.String(15), nullable=False)
    experience = db.Column(db.String(50))
    specialization = db.Column(db.String(100))

    
