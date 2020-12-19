from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, This is the Main page!"

@app.route("/register")
def register():
    return "Hello, This is the Register page!"

@app.route("/booking")
def booking():
    return "Hello, This is the Booking page!"

@app.route("/check-in")
def checkin():
    return "Hello, This is the Checking-in page!"

@app.route("/payment")
def payment():
    return "Hello, This is the Payment page!"