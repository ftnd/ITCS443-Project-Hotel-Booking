# Tanadon Sangkhatorn 6188060
# Thanyanit Jongjitragan 6188075

from flask import Flask, redirect, url_for, render_template, request

import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

# Obtain connection string information from Azure portal
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
    # cursor.execute("SELECT * FROM room;")
    # rows = cursor.fetchall()
    # print("Read",cursor.rowcount,"row(s) of data.")

# Print all rows
    # for row in rows:
    # 	print("Data row = (%s, %s)" %( str(row[0]), str(row[1]) ))

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/register",methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        
        # Obtain data in Form
        fname = request.form['Firstname']
        lname = request.form['Lastname']
        roomtype = request.form['RoomType']
        sdate = request.form['StartDate']
        edate = request.form['EndDate']

        # Get rooms from database 
        # cursor.execute("SELECT * FROM room;")
        # rows = cursor.fetchall()
        # for row in rows:
    	#     print("Data row = (%s, %s)" %( str(row[0]), str(row[1]) ))
        return redirect(url_for('payment'))
    else:
        countSingle = 0
        countDouble = 0
        countSuite = 0
        countKing = 0
        cursor.execute("SELECT * FROM room where 'STATUS' = 0")
        rows = cursor.fetchall()
        for row in rows:
    	    if str(row[2]) == 'single':
                countSingle += 1
    	    if str(row[2]) == 'double':
                countDouble += 1
    	    if str(row[2]) == 'suite':
                countSuite += 1
    	    if str(row[2]) == 'king':
                countKing += 1
        return render_template("register.html", countSingle = countSingle, countDouble = countDouble, countSuite = countSuite, countKing = countKing)

@app.route("/check-in/<name>")
def checkin():
    return "Hello, This is the Checking-in page!"

@app.route("/payment")
def payment():
    title = ""
    return "Hello, This is the Payment page!"


# Close Database Connection
# conn.commit()
# cursor.close()
# conn.close()
# print("Close database successfully.")