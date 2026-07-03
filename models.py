from extensions import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    passhash = db.Column(db.String(200), nullable=False)
    name= db.Column(db.String(50), nullable=False)


class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)



class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"), nullable=False)

    booking_date = db.Column(db.String(20), nullable=False)
    persons = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)


class StaffProfile(db.Model):
    __tablename__ = "staff_profiles"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    phone = db.Column(db.String(15), nullable=False)
    experience = db.Column(db.String(50))
    specialization = db.Column(db.String(100))