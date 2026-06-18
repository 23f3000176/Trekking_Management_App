from controller.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


# =====================
# USER MODEL
# =====================
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    name = db.Column(db.String(100), nullable=False)

    contact = db.Column(db.String(20))

    role = db.Column(db.String(20), nullable=False)# Admin / Staff / User

    status = db.Column(db.String(20), default="Pending")# Pending / Approved / Blacklisted

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship("Booking",backref="user",lazy=True)

    assigned_treks = db.relationship("Trek",backref="staff",lazy=True)

    @property
    def password(self):
        raise AttributeError("Password is not readable")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )

    def __repr__(self):
        return f"<User {self.username}>"


# =====================
# TREK MODEL
# =====================
class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)

    trek_name = db.Column(db.String(100), nullable=False)

    location = db.Column(db.String(100), nullable=False)

    difficulty = db.Column(db.String(20), nullable=False)# Easy / Moderate / Hard

    duration = db.Column(db.Integer, nullable=False)

    available_slots = db.Column(db.Integer, nullable=False)

    description = db.Column(db.Text)

    start_date = db.Column(db.Date, nullable=False)

    end_date = db.Column(db.Date, nullable=False)

    status = db.Column(db.String(20), default="Open")# Open / Closed / Completed

    assigned_staff_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    created_at = db.Column(db.DateTime,default=datetime.utcnow)

    bookings = db.relationship("Booking",backref="trek",lazy=True)

    def __repr__(self):
        return f"<Trek {self.trek_name}>"


# =====================
# BOOKING MODEL
# =====================
class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)

    trek_id = db.Column(db.Integer,db.ForeignKey("treks.id"),nullable=False)

    booking_date = db.Column(db.DateTime,default=datetime.utcnow)

    status = db.Column(db.String(20),default="Booked")# Booked / Cancelled / Completed

    def __repr__(self):
        return f"<Booking {self.id}>"
