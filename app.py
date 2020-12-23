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

# # Read data
# cursor.execute("SELECT * FROM room;")
# rows = cursor.fetchall()
# print("Read",cursor.rowcount,"row(s) of data.")

# # Print all rows
# for row in rows:
#     print("Data row = (%s, %s, %s, %s)" %( str(row[0]), str(row[1]), str(row[2]), str(row[3]) ))

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/booking",methods = ['POST', 'GET'])
def booking():
    if request.method == 'POST':
        
        # Obtain data in Form
        fname = request.form['firstname']
        lname = request.form['lastname']
        roomtype = request.form['RoomType']
        sdate = request.form['startDate']
        edate = request.form['endDate']

        # Get rooms from database 
        cursor.execute("SELECT * FROM room where status = 'available' AND name = LOWER('"+roomtype+"')")
        rows = cursor.fetchall()
        print("Read",cursor.rowcount,"row(s) of data.")
        rid = -1
        for row in rows:
            rid = int(str(row[0]))
            break
        if cursor.rowcount == 0:
            return render_template("booking.html", err = -1, msg = "Selected room is unavailable.")
        return redirect(url_for('payment', fname = fname, lname = lname, rid = rid, sdate = sdate, edate = edate))
    else:
        countSingle = 0; countDouble = 0; countSuite = 0; countKing = 0
        priceSingle = -1; priceDouble = -1; priceSuite = -1; priceKing= -1
        cursor.execute("SELECT * FROM room WHERE status = 'available'")
        rows = cursor.fetchall()
        for row in rows:
    	    if str(row[1]) == 'single':
                countSingle += 1
                priceSingle = str(row[2])
    	    if str(row[1]) == 'double':
                countDouble += 1
                priceDouble = str(row[2])
    	    if str(row[1]) == 'suite':
                countSuite += 1
                priceSuite = str(row[2])
    	    if str(row[1]) == 'king':
                countKing += 1
                priceKing = str(row[2])
        return render_template( "booking.html",
                countSingle = countSingle, countDouble = countDouble, countSuite = countSuite, countKing = countKing,
                priceSingle = priceSingle, priceDouble = priceDouble, priceSuite = priceSuite, priceKing = priceKing
            )

@app.route("/check-in")
def checkin():
    return "Hello, This is the Checking-in page!"

@app.route("/payment",methods = ['POST', 'GET'])
def payment():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        rid = request.form['rid']
        sdate = request.form['sdate']
        edate = request.form['edate']
        cursor.execute("UPDATE room SET status = 1 WHERE 'id' = '"+rid+"' AND 'status' = 'available';")
        rows = cursor.fetchall()
        result = rows.rowcount
        if result == 0:
            return "Payment fail."
        else:
            # cursor.execute("INSERT INTO reservation ()")
            return "Payment success. Your room is reserved."
    else:
        fname = request.args.get('fname',None)
        lname = request.args.get('lname',None)
        rid = request.args.get('rid', None)
        sdate = request.args.get('sdate',None)
        edate = request.args.get('edate',None)
        return "This is the Payment page!<br>Customer: %s %s<br>Room ID: %s<br>From: %s  To: %s" %(fname,lname,rid,sdate,edate)


# # Close Database Connection
# conn.commit()
# cursor.close()
# conn.close()
# print("Close database successfully.")