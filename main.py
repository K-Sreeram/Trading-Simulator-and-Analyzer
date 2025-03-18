# integrate HTML with the flask
# HTTP verb GET and POST

from flask import Flask, redirect, url_for, render_template, request, flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Needed for flashing messages
app.secret_key = 'your_secret_key'  

# connect to MYSQL database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'  # Later replace with MySQL URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# For database migrations
migrate = Migrate(app, db)  

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# -------------------- Routes ------------------------

# Home route (Login Page)
@app.route('/')
def loginPage():
    return render_template('login.html')


# Register Page route
@app.route('/register', methods=["GET", "POST"])
def registerPage():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']  # Field name should match HTML form

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match. Please try again.")
            return redirect(url_for('registerPage'))

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists! Please choose a different username.")
            return redirect(url_for('registerPage'))

        # Hash the password before storing
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Add new user to DB
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.")
        return redirect(url_for('loginPage'))  # Assuming '/' is loginPage

    return render_template('register.html')


# Login route
@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            flash("Login Successful!")
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for('welcome'))  # Redirect to welcome or home page after login
        else:
            flash("Invalid Username or Password!")
            return redirect(url_for('loginPage'))

    return redirect(url_for('loginPage'))

@app.route('/test_db')
def test_db():
    users = User.query.all()
    return f"Found {len(users)} users"

@app.route("/welcome")
def welcome():
    if "user_id" in session:
        return render_template("welcome.html",username=session["username"])
    else:
        return redirect(url_for("loginPage"))
    
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")
    
# -------------------- Main ------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

