# Tanadon Sangkhatorn 6188060
# Thanyanit Jongjitragan 6188075

from flask import Flask, redirect, url_for, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'hotelmysql.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'hoteldb060075@hotelmysql'
app.config['MYSQL_PASSWORD'] = 'Admin060075'
app.config['MYSQL_DB'] = 'hoteldb'
 
mysql = MySQL(app)


@app.route("/")
@app.route("/index")
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM room")
    rows = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()
    print("Read",cursor.rowcount,"row(s) of data.")
    for row in rows:
        print(str(row[0])+" "+str(row[1])+" "+str(row[2])+" "+str(row[3])+" ")
    
    return render_template("index.html")

@app.route("/bookdate",methods = ['POST', 'GET'])
def bookdate():
    if request.method == 'POST':
        sdate = request.form['startDate']
        edate = request.form['endDate']
        return redirect(url_for('booking',sdate = sdate, edate = edate))
    else:
        return render_template("booking-selectdate.html")

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
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM room where status = 'available' AND name = LOWER('"+roomtype+"')")
        rows = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
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
        sdate = request.args.get('sdate',None)
        edate = request.args.get('edate',None)

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM room WHERE id NOT IN (SELECT rid FROM reservation WHERE startDate < '"+edate+"' AND endDate > '"+sdate+"');")
        rows = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
        print("Read",cursor.rowcount,"row(s) of available room.")

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
        fname = request.form['firstname']
        lname = request.form['lastname']
        rid = request.form['roomNO']
        sdate = request.form['startDate']
        edate = request.form['endDate']

        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE room SET status = 'reserved' WHERE 'id' = '"+rid+"' AND 'status' = 'available';")
        rows = cursor.fetchall()
        result = cursor.rowcount
        mysql.connection.commit()
        cursor.close()

        if result == 0:
            return "payment fail"
        else:
            # cursor.execute("INSERT INTO reservation ()")
            return "reservation success"
    
    else:
        fname = request.args.get('fname',None)
        lname = request.args.get('lname',None)
        rid = request.args.get('rid', None)
        sdate = request.args.get('sdate',None)
        edate = request.args.get('edate',None)
        return render_template( "payment.html",
                fname = fname, lname = lname, rid = rid, sdate = sdate, edate = edate, msg = "payment success"
            )


if __name__ == '__main__':
    app.run()