from flask import Flask, render_template, request, redirect, url_for, flash
from scraper import compare_price
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# ---------------- SECRET KEY ----------------
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "fallback-secret")

# ---------------- DATABASE CONFIG ----------------
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is not set. Check Railway variables.")

# Fix postgres:// → postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------- LOGIN MANAGER ----------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ---------------- USER MODEL ----------------
class User(UserMixin, db.Model):
    __tablename__ = "user"   # 🔥 important for Postgres

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# ---------------- PRODUCT MODEL ----------------
class Product(db.Model):
    __tablename__ = "product"   # 🔥 important

    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(200))
    price = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# ---------------- CREATE DATABASE ----------------
@app.before_request
def create_tables():
    db.create_all()   # ✅ ensures tables exist in PostgreSQL

# ---------------- LOAD USER ----------------
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ---------------- HOME ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
@login_required
def home():

    result = None

    if request.method == "POST":
        product = request.form["product"]
        stores = request.form.getlist("store")
        result = compare_price(product, stores)

    return render_template("index.html", result=result)

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists!")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        user = User(username=username, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        flash("Account created! Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials")

    return render_template("login.html")

# ---------------- LOGOUT ----------------
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ---------------- TRACK ROUTE ----------------
@app.route("/track", methods=["POST"])
@login_required
def track():

    product = request.form["product"]
    phone = request.form["phone"]
    price = request.form.get("price")

    if price:
        try:
            price = int(price.replace(",", "").strip())
        except:
            price = None

    new_product = Product(
        product=product,
        price=price,
        phone=phone,
        user_id=current_user.id
    )

    db.session.add(new_product)
    db.session.commit()

    return "Product added for price tracking!"

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)