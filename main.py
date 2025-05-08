from flask import Flask, redirect, url_for, render_template, request, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from utils.data import stock_names
from werkzeug.security import generate_password_hash, check_password_hash
from utils.get_data import get_stock_data, get_live_stock_data, generate_combined_graph
import yfinance as yf
import numpy as np
import pandas as pd
import os
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from datetime import datetime, timedelta

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

# -------------------- Helper Functions for Prediction ------------------------

def prepare_data(stock_symbol, lookback=60):
    try:
        # Fetch historical data (last 2 years for training)
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
        stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
        if stock_data.empty:
            raise ValueError("No historical data available for this stock")

        # Extract features: Close price, Volume, and 10-day Simple Moving Average
        close_prices = stock_data['Close'].values
        volume = stock_data['Volume'].values
        sma_10 = stock_data['Close'].rolling(window=10).mean().fillna(method='bfill').values

        # Combine features into a single array
        features = np.column_stack((close_prices, volume, sma_10))

        # Scale the data
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(features)

        # Prepare sequences for LSTM
        X, y = [], []
        for i in range(lookback, len(scaled_data)):
            X.append(scaled_data[i-lookback:i])
            y.append(scaled_data[i, 0])  # Predict the Close price
        X, y = np.array(X), np.array(y)

        return X, y, scaler, scaled_data, close_prices
    except Exception as e:
        print(f"Error preparing data for {stock_symbol}: {str(e)}")
        raise

def build_lstm_model(lookback=60, num_features=3):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(lookback, num_features)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# -------------------- Routes ------------------------

# Initialize Database within Application Context
with app.app_context():
    db.create_all()

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
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match. Please try again.")
            return redirect(url_for('registerPage'))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists! Please choose a different username.")
            return redirect(url_for('registerPage'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please login.")
        return redirect(url_for('loginPage'))

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
            return redirect(url_for('welcome'))
        else:
            flash("Invalid Username or Password!")
            return redirect(url_for('loginPage'))

    return redirect(url_for('loginPage'))

@app.route('/test_db')
def test_db():
    users = User.query.all()
    return f"Found {len(users)} users"

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect(url_for('loginPage'))

@app.route("/welcome")
def welcome():
    if "user_id" in session:
        return render_template("welcome.html", username=session["username"])
    else:
        return redirect(url_for("loginPage"))

@app.route("/dashboard")
def dashboard():
    if "user_id" in session:
        return render_template("dashboard.html", username=session["username"])
    return redirect(url_for("loginPage"))

@app.route("/plot")
def plot():
    stocks = stock_names
    return render_template("plot.html", stocks=stocks)

@app.route("/compare")
def compare():
    stocks = stock_names
    return render_template("compare.html", stocks=stocks)

@app.route("/api/stock", methods=["GET"])
def get_stock_data_api():
    selected_stock = request.args.get("stock")
    data = get_live_stock_data(selected_stock)
    return data

@app.route("/api/plot", methods=["GET"])
def get_plot():
    selected_stock = request.args.get("stock")
    selected_criteria = request.args.get("criteria")
    start_date = request.args.get("begin")
    end_date = request.args.get("end")
    image_path = get_stock_data(selected_stock, start_date, end_date, selected_criteria)
    print("Image Path: ", image_path)
    json_data = {"image_path": image_path}
    return json_data

@app.route("/api/compare", methods=["POST"])
def get_compare_plot():
    data = request.get_json()
    selected_stocks = data["stocks"]
    selected_criteria = data["criteria"]
    start_date = data["begin"]
    end_date = data["end"]
    image_path = generate_combined_graph(selected_criteria, selected_stocks, start_date, end_date)
    print("Image Path: ", image_path)
    json_data = {"image_path": image_path}
    return json_data

@app.route("/api/liveData", methods=["GET"])
def get_live_data():
    df = get_live_stock_data()
    json_data = df.to_json(orient="records")
    return json_data

@app.route("/api/predict", methods=["GET"])
def predict_stock_price():
    stock_symbol = request.args.get("stock")
    if not stock_symbol:
        return jsonify({"error": "Stock symbol is required"}), 400
    try:
        print(f"Predicting for stock: {stock_symbol}")
        # Check if model exists for this stock
        model_path = f"models/{stock_symbol}_model.h5"
        if os.path.exists(model_path):
            print(f"Loading existing model from {model_path}")
            model = load_model(model_path)
        else:
            print("Training new model...")
            # Prepare data and train model
            X, y, scaler, scaled_data, close_prices = prepare_data(stock_symbol)
            train_size = int(len(X) * 0.8)
            X_train, X_test = X[:train_size], X[train_size:]
            y_train = y[:train_size]

            model = build_lstm_model()
            model.fit(X_train, y_train, epochs=5, batch_size=32, verbose=0)

            # Save the model
            if not os.path.exists("models"):
                os.makedirs("models")
            model.save(model_path)
            print(f"Model saved to {model_path}")

        # Prepare input for prediction (last 60 days)
        X, y, scaler, scaled_data, close_prices = prepare_data(stock_symbol)
        last_sequence = scaled_data[-60:]

        # Predict next day's price
        predicted_scaled = model.predict(last_sequence.reshape(1, 60, 3), verbose=0)
        predicted_price = scaler.inverse_transform(
            np.concatenate([predicted_scaled, np.zeros((1, 2))], axis=1)
        )[0, 0]

        # Get the latest closing price for context
        stock_data = yf.download(stock_symbol, period="1d")
        if stock_data.empty:
            raise ValueError("No recent data available for this stock")
        latest_price = stock_data['Close'].iloc[-1]

        return jsonify({
            "stock": stock_symbol,
            "latest_price": round(float(latest_price), 2),
            "predicted_price": round(float(predicted_price), 2),
            "prediction_date": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        })
    except Exception as e:
        print(f"Error predicting for {stock_symbol}: {str(e)}")
        return jsonify({"error": str(e)}), 500

# -------------------- Main ------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)