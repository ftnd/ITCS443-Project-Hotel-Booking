from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/booking")
def booking():
    return "Hello, This is the Booking page!"

@app.route("/check-in")
def checkin():
    return "Hello, This is the Checking-in page!"

@app.route("/payment")
def payment():
    return "Hello, This is the Payment page!"

@app.route("/test")
def test():
    return "Test Test Test"