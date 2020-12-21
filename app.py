from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    title = ""
    return render_template("home.html", title = title)

@app.route("/register")
def register():
    title = ""
    return render_template("register.html", title = title)

@app.route("/booking")
def booking():
    title = ""
    return "Hello, This is the Booking page!"

@app.route("/check-in")
def checkin():
    title = ""
    return "Hello, This is the Checking-in page!"

@app.route("/payment")
def payment():
    title = ""
    return "Hello, This is the Payment page!"

@app.route("/test")
def test():
    return "Test Test Test"