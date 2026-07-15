from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models import Booking, StaffProfile, Trek, User

from extensions import db

from datetime import datetime

main = Blueprint("main", __name__)


@main.route("/")
def home():
    if 'user_id' not in session:
        flash("Please log in to access this page.")
        return render_template("login.html")
    return render_template("home.html" , user=User.query.get(session["user_id"]))


# loginnn page =======================================
@main.route("/login")
def login():
    return render_template("login.html")

@main.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("Invalid username or password")
        return render_template("login.html")
    if not user.check_password(password):
        flash("Invalid username or password")
        return render_template("login.html")
    if user.role == "staff" and not user.approved:
        flash("Your account is not approved yet. Please wait for admin approval.")
        return render_template("login.html")
    
    if not user.active:
        flash("Your account is deactivated. Please contact the admin.")
        return render_template("login.html")
    # Login successful
    session["user_id"] = user.id
    session["role"] = user.role
    if user.role == "admin":
        return redirect(url_for("main.admin_dashboard"))

    elif user.role == "staff":
        return redirect(url_for("main.staff_dashboard"))

    else:
        return redirect(url_for("main.user_dashboard"))
    


#register page =======================================
@main.route("/register")
def register():
    return render_template("register.html")

@main.route("/register", methods=["POST"])
def register_post():
    username = request.form.get("username")
    password = request.form.get("password")
    name = request.form.get("name")
    role = request.form.get("role")
   
    
    if User.query.filter_by(username=username).first():
        flash("Username already exists")
        return render_template("register.html")
    user=User(username=username, name=name, role=role)
    if role == "customer":
        user.approved = True  
    user.password = password  # This will trigger the password setter and hash the password
    db.session.add(user)
    db.session.commit()
    flash("Registration successful. Please log in.")
    return render_template("login.html")



#logout page =======================================
@main.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out successfully.")
    return redirect(url_for("main.login"))


#admin dashboard-----------------------------

@main.route("/admin/dashboard")
def admin_dashboard():

    if session.get("role") != "admin":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    total_users = User.query.filter_by(role="customer").count()

    total_staff = User.query.filter_by(role="staff").count()

    total_treks = Trek.query.count()

    total_bookings = Booking.query.count()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_staff=total_staff,
        total_treks=total_treks,
        total_bookings=total_bookings
    )



#admin - treks management-----------------------------
@main.route("/admin/add_trek")
def add_trek():
    if session.get("role") != "admin":
        flash("Access Denied!")
        return redirect(url_for("main.login"))
    return render_template("admin/add_trek.html")

@main.route("/admin/add_trek", methods=["POST"])
def add_trek_post():
    if session.get("role") != "admin":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    name = request.form.get("name")
    location = request.form.get("location")
    difficulty = request.form.get("difficulty")
    duration = request.form.get("duration")
    price = request.form.get("price")
    available_slots = request.form.get("available_slots")
    assigned_staff_id = request.form.get("assigned_staff_id")
    status = request.form.get("status")

    trek = Trek(
        name=name,
        location=location,
        difficulty=difficulty,
        duration=duration,
        price=price,
        available_slots=available_slots,
        assigned_staff_id=assigned_staff_id,
        status=status
    )

    db.session.add(trek)
    db.session.commit()

    flash("Trek Added Successfully")

    return redirect(url_for("main.admin_dashboard"))


@main.route("/admin/view_treks")
def view_treks():
    if session.get("role") != "admin":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    treks = Trek.query.all()

    return render_template("admin/view_treks.html",treks=treks)

@main.route("/admin/edit_trek/<int:trek_id>")
def edit_trek(trek_id):
    if session.get("role") != "admin":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    trek = Trek.query.get_or_404(trek_id)

    staff = User.query.filter_by(role="staff").all()

    return render_template(
        "admin/edit_trek.html",
        trek=trek,
        staff=staff
    )

@main.route("/admin/edit_trek/<int:trek_id>", methods=["POST"])
def edit_trek_post(trek_id):
    if session.get("role") != "admin":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    trek = Trek.query.get_or_404(trek_id)

    trek.name = request.form.get("name")
    trek.location = request.form.get("location")
    trek.difficulty = request.form.get("difficulty")
    trek.duration = request.form.get("duration")
    trek.price = request.form.get("price")
    trek.available_slots = request.form.get("available_slots")
    trek.assigned_staff_id = request.form.get("assigned_staff")
    trek.status = request.form.get("status")

    db.session.commit()

    flash("Trek updated successfully.")

    return redirect(url_for("main.view_treks"))


@main.route("/admin/delete_trek/<int:trek_id>")
def delete_trek(trek_id):
    if session.get("role") != "admin":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    trek = Trek.query.get_or_404(trek_id)

    db.session.delete(trek)
    db.session.commit()

    flash("Trek deleted successfully.")
    return redirect(url_for("main.view_treks"))



#admin - staff management-----------------------------
@main.route("/admin/view_staff")
def view_staff():
    if session.get("role") != "admin":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    staff_members = User.query.filter_by(role="staff").all()

    return render_template("admin/view_staff.html", staff=staff_members)

@main.route("/admin/approve_staff/<int:user_id>")
def approve_staff(user_id):

    if session.get("role") != "admin":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    user = User.query.get_or_404(user_id)

    user.approved = True

    db.session.commit()

    flash("Staff approved successfully.")

    return redirect(url_for("main.view_staff"))

@main.route("/admin/view_users")
def view_users():

    if session.get("role") != "admin":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    users = User.query.filter_by(role="customer").all()

    return render_template(
        "admin/view_users.html",
        users=users
    )




#staff dashboard-----------------------------
@main.route("/staff/dashboard")
def staff_dashboard():
    if session.get("role") != "staff":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    user_id = session.get("user_id")

    treks = Trek.query.filter_by(assigned_staff_id=user_id).all()

    return render_template(
        "staff/dashboard.html",
        staff=User.query.get(session["user_id"]),
        treks=treks
    )



@main.route("/staff/profile")
def staff_profile():

    if session.get("role") != "staff":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    profile = StaffProfile.query.filter_by(
        user_id=session["user_id"]
    ).first()

    return render_template(
        "staff/profile.html",
        profile=profile
    )

@main.route("/staff/profile", methods=["POST"])
def staff_profile_post():

    if session.get("role") != "staff":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    profile = StaffProfile.query.filter_by(
        user_id=session["user_id"]
    ).first()

    if profile is None:
        profile = StaffProfile(user_id=session["user_id"])
        db.session.add(profile)

    profile.phone = request.form.get("phone")
    profile.experience = request.form.get("experience")
    profile.specialization = request.form.get("specialization")

    db.session.commit()

    flash("Profile updated successfully.")

    return redirect(url_for("main.staff_dashboard"))


@main.route("/admin/delete_staff/<int:user_id>")
def delete_staff(user_id):

    if session.get("role") != "admin":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    staff = User.query.get_or_404(user_id)

    if staff.role != "staff":
        flash("Only staff members can be removed.")
        return redirect(url_for("main.view_staff"))

    # Remove staff assignment from all treks
    treks = Trek.query.filter_by(assigned_staff_id=staff.id).all()

    for trek in treks:
        trek.assigned_staff_id = None

    db.session.delete(staff)
    db.session.commit()

    flash("Staff removed successfully.")

    return redirect(url_for("main.view_staff"))


@main.route("/admin/search")
def search():

    if session.get("role") != "admin":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    query = request.args.get("query", "").strip()
    if not query:
        flash("Please enter a search term.")
        return redirect(url_for("main.admin_dashboard"))

    treks = Trek.query.filter(
        Trek.name.ilike(f"%{query}%")
    ).all()

    staff = User.query.filter(
        User.role == "staff",
        User.name.ilike(f"%{query}%")
    ).all()

    users = User.query.filter(
        User.role == "customer",
        User.name.ilike(f"%{query}%")
    ).all()

    return render_template(
        "admin/search.html",
        treks=treks,
        staff=staff,
        users=users,
        query=query
    )

@main.route("/admin/deactivate_user/<int:user_id>")
def deactivate_user(user_id):

    if session.get("role") != "admin":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    user = User.query.get_or_404(user_id)

    user.active = False

    db.session.commit()

    flash("User deactivated successfully.")

    return redirect(url_for("main.view_users"))


@main.route("/admin/view_bookings")
def view_bookings():

    if session.get("role") != "admin":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    bookings = Booking.query.all()

    return render_template(
        "admin/view_bookings.html",
        bookings=bookings
    )

@main.route("/staff/update_status/<int:trek_id>")
def update_trek_status(trek_id):

    if session.get("role") != "staff":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    trek = Trek.query.get_or_404(trek_id)
    if trek.assigned_staff_id != session["user_id"]:
        flash("You can update only your assigned treks.")
        return redirect(url_for("main.staff_dashboard"))

    return render_template(
        "staff/update_status.html",
        trek=trek
    )

@main.route("/staff/update_status/<int:trek_id>", methods=["POST"])
def update_trek_status_post(trek_id):

    if session.get("role") != "staff":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    trek = Trek.query.get_or_404(trek_id)
    if trek.assigned_staff_id != session["user_id"]:
        flash("You can update only your assigned treks.")
        return redirect(url_for("main.staff_dashboard"))

    trek.status = request.form.get("status")

    db.session.commit()

    flash("Trek status updated successfully.")

    return redirect(url_for("main.staff_dashboard"))


@main.route("/staff/update_slots/<int:trek_id>")
def update_slots(trek_id):

    if session.get("role") != "staff":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    trek = Trek.query.get_or_404(trek_id)

    if trek.assigned_staff_id != session["user_id"]:
        flash("You can update only your assigned treks.")
        return redirect(url_for("main.staff_dashboard"))

    return render_template(
        "staff/update_slots.html",
        trek=trek
    )

@main.route("/staff/update_slots/<int:trek_id>", methods=["POST"])
def update_slots_post(trek_id):

    if session.get("role") != "staff":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    trek = Trek.query.get_or_404(trek_id)

    if trek.assigned_staff_id != session["user_id"]:
        flash("You can update only your assigned treks.")
        return redirect(url_for("main.staff_dashboard"))

    trek.available_slots = request.form.get("available_slots")

    db.session.commit()

    flash("Available slots updated successfully.")

    return redirect(url_for("main.staff_dashboard"))



@main.route("/user/dashboard")
def user_dashboard():

    if session.get("role") != "customer":
        flash("Access Denied!")
        return redirect(url_for("main.login"))
    

    search = request.args.get("search", "")
    difficulty = request.args.get("difficulty", "")

    treks = Trek.query.filter(Trek.status == "Open")

    if search:
        treks = treks.filter(Trek.name.ilike(f"%{search}%"))

    if difficulty:
        treks = treks.filter(Trek.difficulty == difficulty)

    treks = treks.all()


    return render_template(
        "user/dashboard.html",
        treks=treks
    )


@main.route("/user/book/<int:trek_id>")
def book_trek(trek_id):

    if session.get("role") != "customer":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    trek = Trek.query.get_or_404(trek_id)

    return render_template("user/book_trek.html",trek=trek)

@main.route("/user/book/<int:trek_id>", methods=["POST"])
def book_trek_post(trek_id):

    if session.get("role") != "customer":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    trek = Trek.query.get_or_404(trek_id)

    if trek.status != "Open":
        flash("This trek is not open for booking.")
        return redirect(url_for("main.user_dashboard"))

    existing_booking = Booking.query.filter_by(user_id=session["user_id"],trek_id=trek.id).first()

    if existing_booking:
        flash("You have already booked this trek.")
        return redirect(url_for("main.user_dashboard"))

    persons = int(request.form.get("persons"))
    if trek.available_slots < persons:
        flash("Not enough slots available.")
        return redirect(url_for("main.user_dashboard"))

    booking = Booking(
        user_id=session["user_id"],
        trek_id=trek.id,
        booking_date=datetime.now().strftime("%Y-%m-%d"),
        persons=persons,
        total_price=persons * trek.price,
        booking_status="Booked",
        payment_status="Pending"
    )

    db.session.add(booking)

    trek.available_slots -= persons

    db.session.commit()

    flash("Trek booked successfully!")

    return redirect(url_for("main.user_dashboard"))


@main.route("/user/my_bookings")
def my_bookings():

    if session.get("role") != "customer":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    bookings = Booking.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "user/my_bookings.html",
        bookings=bookings
    )


@main.route("/user/cancel_booking/<int:booking_id>")
def cancel_booking(booking_id):

    if session.get("role") != "customer":
        flash("Access Denied!")
        return redirect(url_for("main.login"))

    booking = Booking.query.get_or_404(booking_id)

    if booking.user_id != session["user_id"]:
        flash("Access Denied!")
        return redirect(url_for("main.my_bookings"))

    if booking.booking_status != "Booked":
        flash("Booking cannot be cancelled.")
        return redirect(url_for("main.my_bookings"))

    trek = Trek.query.get(booking.trek_id)

    trek.available_slots += booking.persons

    booking.booking_status = "Cancelled"

    db.session.commit()

    flash("Booking cancelled successfully.")

    return redirect(url_for("main.my_bookings"))