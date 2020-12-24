# Tanadon Sangkhatorn 6188060
# Thanyanit Jongjitragan 6188075

from flask import Flask, redirect, url_for, render_template, request
from flask_mysqldb import MySQL
from datetime import datetime

# Function to calculate day differrent between two dates (YYYY-MM-DD)
def days_count(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    # +1 to count one more days: from days 24 to 25 --> |(25-24)| + 1 = 2 days
    return abs((d2 - d1).days)+1

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'hotelmysql.mysql.database.azure.com'
app.config['MYSQL_USER'] = 'hoteldb060075@hotelmysql'
app.config['MYSQL_PASSWORD'] = 'Admin060075'
app.config['MYSQL_DB'] = 'hoteldb'
 
mysql = MySQL(app)


    
@app.route("/")
@app.route("/index")
def index():    
    return render_template("index.html")

@app.route("/bookdate",methods = ['POST', 'GET'])
def dateBook():
    if request.method == 'POST':
        sdate = request.form['startDate']
        edate = request.form['endDate']
        return redirect(url_for('booking',sdate = sdate, edate = edate))
    else:
        return render_template("booking-selectdate.html")

@app.route("/booking",methods = ['POST', 'GET'])
def booking():
    msg = ""
    if request.method == 'POST':
        # Obtain data in Form
        fname = request.form['firstname']
        lname = request.form['lastname']
        roomtype = request.form['RoomType']
        sdate = request.form['startDate']
        edate = request.form['endDate']

        # Get rooms from database 
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM room WHERE name = '"+roomtype+"' AND id NOT IN (SELECT rid FROM reservation WHERE startDate < '"+edate+"' AND endDate > '"+sdate+"');")
        rows = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
        print("Read",cursor.rowcount,"row(s) of available room for selected date range.")

        if cursor.rowcount == 0:
            msg = "No "+roomtype+" is available for the selected date range."
            
        else:
            # Get room number
            rid = -1
            for row in rows:
                rid = int(str(row[0]))
                break
            return redirect(url_for('payment', fname = fname, lname = lname, rid = rid, sdate = sdate, edate = edate))
    
    countSingle = 0; countDouble = 0; countSuite = 0; countKing = 0
    priceSingle = -1; priceDouble = -1; priceSuite = -1; priceKing= -1
    fname = ''; lname = ''; sdate = ''; edate = ''
    if request.method == 'POST':
        fname = request.form['firstname']
        lname = request.form['lastname']
        sdate = request.form['startDate']
        edate = request.form['endDate']
    else:
        sdate = request.args.get('sdate',None)
        edate = request.args.get('edate',None)

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM room WHERE id NOT IN (SELECT rid FROM reservation WHERE startDate < '"+edate+"' AND endDate > '"+sdate+"');")
    print("Read",cursor.rowcount,"row(s) of available room.")
    rows = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()

    # Count available room for each room type
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
            priceSingle = priceSingle, priceDouble = priceDouble, priceSuite = priceSuite, priceKing = priceKing,
            fname = fname, lname = lname,sdate = sdate, edate = edate, msg = msg
        )

@app.route("/checkin",methods = ['POST', 'GET'])
def checkin():
    err = ''; msg=''
    if request.method == 'POST':
        fname = request.form['firstname']
        lname = request.form['lastname']
        code = request.form['code']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM reservation WHERE id = '"+code+"' AND fname = '"+fname+"' AND lname = '"+lname+"';")
        print("Read",cursor.rowcount,"row(s) of reservation verification.")
        rows = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()

        if cursor.rowcount == 1:
            for row in rows:
                msg = "Check-in SUCCESS. Your room number is "+str(row[3])+". Please check-out within "+str(row[5])+". Enjoy your stay!"
        else:
            err = "Check-in fail"
            
    return render_template("check-in.html",err=err,msg=msg)

@app.route("/payment",methods = ['POST', 'GET'])
def payment():
    if request.method == 'POST':
        fname = request.form['firstname']
        lname = request.form['lastname']
        rid = request.form['roomNO']
        sdate = request.form['startDate']
        edate = request.form['endDate']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO reservation (fname,lname,rid,startDate,endDate,dateBook) VALUES ('"+fname+"','"+lname+"','"+rid+"','"+sdate+"','"+edate+"',CURDATE())")
        print("INSERT",cursor.rowcount,"row(s) of reservation.")
        cursor.execute("SELECT * FROM reservation WHERE rid = '"+rid+"' AND fname = '"+fname+"' AND lname = '"+lname+"' AND startDate = '"+sdate+"' AND endDate = '"+edate+"';")
        rows = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
        code = ''
        for row in rows:
            print(str(row[0])+" "+str(row[1])+" "+str(row[2])+" "+str(row[3])+" "+str(row[4])+" "+str(row[5])+" "+str(row[6]))
            code = str(row[0])

        return render_template("payment-successful.html", code = code)
    
    else:
        fname = request.args.get('fname',None)
        lname = request.args.get('lname',None)
        rid = request.args.get('rid', None)
        sdate = request.args.get('sdate',None)
        edate = request.args.get('edate',None)
        return render_template( "payment.html",
                fname = fname, lname = lname, rid = rid, sdate = sdate, edate = edate, msg = "payment success"
            )

@app.route("/report")
def report():
    pdc = ""; pmc = ""; rsc = ""
    return render_template("report.html",perdaycode=pdc,permonthcode=pmc,roomstatcode=rsc)

@app.route("/perday",methods = ['POST', 'GET'])
def perday():
    pdc = ""; pmc = ""; rsc = ""
    if request.method == 'POST':
        date = request.form['startDate']
        single = 0; double = 0; suite = 0; king = 0; total = 0

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM reservation WHERE dateBook = '"+date+"';")
        rows = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()

        for row in rows:
            rid = str(row[3])
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM room WHERE id = '"+rid+"';")
            roomlist = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
            for room in roomlist:
                if rid == str(room[0]):
                    name = str(room[1])
                    if name == "single":
                        single += 1
                    elif name == "double":
                        double += 1
                    elif name == "suite":
                        suite += 1
                    elif name == "king":
                        king += 1
                    break
        total = single + double + suite + king

        pdc = "<tr><td>DATE:"+str(date)+"<br><br>"
        pdc += "<b>Total booking of each room type</b><br>"
        pdc += "Single: "+str(single)+"<br>"
        pdc += "Double: "+str(double)+"<br>"
        pdc += "Suite: "+str(suite)+"<br>"
        pdc += "King: "+str(king)+"<br><br>"
        pdc += "Total booking: "+str(total)
        pdc += "</td></tr>"
    
    return render_template("report.html",perdaycode=pdc,permonthcode=pmc,roomstatcode=rsc)

@app.route("/permonth",methods = ['POST', 'GET'])
def permonth():
    pdc = ""; pmc = ""; rsc = ""
    if request.method == 'POST':
        date = request.form['permonth'] + "-01"
        yearmonth = request.form['permonth']
        single = 0; double = 0; suite = 0; king = 0; total = 0

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM reservation WHERE MONTH(dateBook) = MONTH('"+date+"') AND YEAR(dateBook) = YEAR('"+date+"');")
        rows = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()

        for row in rows:
            rid = str(row[3])
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM room WHERE id = '"+rid+"';")
            roomlist = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
            for room in roomlist:
                if rid == str(room[0]):
                    name = str(room[1])
                    if name == "single":
                        single += 1
                    elif name == "double":
                        double += 1
                    elif name == "suite":
                        suite += 1
                    elif name == "king":
                        king += 1
                    break
        total = single + double + suite + king

        pmc = "<tr><td>YEAR-MONTH:"+str(yearmonth)+"<br><br>"
        pmc += "<b>Total booking of each room type</b><br>"
        pmc += "Single: "+str(single)+"<br>"
        pmc += "Double: "+str(double)+"<br>"
        pmc += "Suite: "+str(suite)+"<br>"
        pmc += "King: "+str(king)+"<br><br>"
        pmc += "Total booking: "+str(total)
        pmc += "</td></tr>"
    
    return render_template("report.html",perdaycode=pdc,permonthcode=pmc,roomstatcode=rsc)

@app.route("/roomstat",methods = ['POST', 'GET'])
def roomstat():
    pdc = ""; pmc = ""; rsc = ""
    if request.method == 'POST':
        sdate = request.form['sdate']
        edate = request.form['edate']

        single = 0; double = 0; suite = 0; king = 0; total = 0

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM reservation WHERE startDate <= '"+edate+"' AND endDate >= '"+sdate+"';")
        rows = cursor.fetchall()
        mysql.connection.commit()
        cursor.close()
        
        for row in rows:
            rid = str(row[3])
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM room WHERE id = '"+rid+"';")
            roomlist = cursor.fetchall()
            mysql.connection.commit()
            cursor.close()
            for room in roomlist:
                if rid == str(room[0]):
                    name = str(room[1])
                    diff = days_count(str(row[4]),str(row[5]))
                    diff = min(diff, days_count(str(row[4]),edate))
                    diff = min(diff, days_count(sdate,str(row[5])))
                    diff = min(diff, days_count(sdate,edate))
                    if name == "single":
                        single += diff
                    elif name == "double":
                        double += diff
                    elif name == "suite":
                        suite += diff
                    elif name == "king":
                        king += diff
                    break
        total = single + double + suite + king

        rsc = "<tr><td>From: "+str(sdate)+"<br>To: "+str(edate)+"<br><br>"
        rsc += "<b>The number of days these room types have been booked for</b><br>"
        rsc += "Single: "+str(single)+"<br>"
        rsc += "Double: "+str(double)+"<br>"
        rsc += "Suite: "+str(suite)+"<br>"
        rsc += "King: "+str(king)+"<br><br>"
        rsc += "Total day of all rooms: "+str(total)
        rsc += "</td></tr>"
    
    return render_template("report.html",perdaycode=pdc,permonthcode=pmc,roomstatcode=rsc)

if __name__ == '__main__':
    app.run()