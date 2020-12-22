from flask import Flask, redirect, url_for, render_template

import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

# Obtain connection string information from the portal
config = {
  'host':'hotelmysql.mysql.database.azure.com',
  'user':'hoteldb060075@hotelmysql',
  'password':'Admin060075',
  'database':'hoteldb'
}

# Construct connection string
try:
  conn = mysql.connector.connect(**config)
  print("Connection established")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with the user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cursor = conn.cursor()

# Read data
  cursor.execute("SELECT * FROM room;")
  rows = cursor.fetchall()
  print("Read",cursor.rowcount,"row(s) of data.")

# Print all rows
  for row in rows:
  	print("Data row = (%s, %s)" %( str(row[0]), str(row[1]) ))

@app.route("/")
def index():
    title = ""
    return render_template("index.html", title = title)

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


# Close Database Connection
conn.commit()
cursor.close()
conn.close()
print("Close database successfully.")