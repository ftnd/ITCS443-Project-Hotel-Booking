from flask import Flask, redirect, url_for, render_template

import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

# Obtain connection string information from the portal
config = {
  'host':'hoteldb060075.database.windows.net',
  'user':'hoteldb060075',
  'password':'Admin060075',
  'database':'hoteldb'
}

# Construct connection string
try:
   conn = mysql.connector.connect(
       user="hoteldb060075@hotelmysql",
       password="Admin060075", 
       host="hotelmysql.mysql.database.azure.com", 
       port=3306, 
      #  database="hoteldb"
       )
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


# Drop previous table of same name if one exists
  cursor.execute("DROP TABLE IF EXISTS inventory;")
  print("Finished dropping table (if existed).")

  # Create table
  cursor.execute("CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
  print("Finished creating table.")

  # Insert some data into table
  cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("banana", 150))
  print("Inserted",cursor.rowcount,"row(s) of data.")
  cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("orange", 154))
  print("Inserted",cursor.rowcount,"row(s) of data.")
  cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("apple", 100))
  print("Inserted",cursor.rowcount,"row(s) of data.")

  # Cleanup
  conn.commit()
  cursor.close()
  conn.close()
  print("Done.")



# @app.route("/")
# def index():
#     title = ""
#     return render_template("index.html", title = title)

# @app.route("/register")
# def register():
#     title = ""
#     return render_template("register.html", title = title)

# @app.route("/booking")
# def booking():
#     title = ""
#     return "Hello, This is the Booking page!"

# @app.route("/check-in")
# def checkin():
#     title = ""
#     return "Hello, This is the Checking-in page!"

# @app.route("/payment")
# def payment():
#     title = ""
#     return "Hello, This is the Payment page!"

# @app.route("/test")
# def test():
#     return "Test Test Test"