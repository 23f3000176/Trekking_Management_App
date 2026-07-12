from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models import Booking, Trek, User

from extensions import db

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
    # Login successful
    session["user_id"] = user.id
    session["role"] = user.role
    if user.role == "admin":
        return redirect(url_for("main.admin_dashboard"))

    elif user.role == "staff":
        return redirect(url_for("main.staff_dashboard"))

    else:
        return redirect(url_for("main.home"))
    


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
    trek.assigned_staff_id = request.form.get("assigned_staff_id")
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