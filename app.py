from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

# For local Testing
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "winery_db"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# For OSU Servers
#app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
#app.config["MYSQL_USER"] = "cs340_OSUusername"
#app.config["MYSQL_PASSWORD"] = "XXXX"
#app.config["MYSQL_DB"] = "cs340_OSUusername"
#app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


# Home Page
@app.route('/')
def root():
    return render_template("main.jinja")

# Customers Main Page
@app.route('/customers', methods=["POST", "GET"])
def customers():
    if request.method == "GET":
        query = "SELECT * FROM Customers"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template('customers.jinja', customers=data)
    
    if request.method == "POST":
        if request.form.get("add_customer"):
            phone_num = request.form["phone_num"]
            email = request.form["email"]
            name = request.form["name"]
            visit_frequency_monthly = request.form["visit_frequency_monthly"]

            if email == "" and visit_frequency_monthly == "":
                query = "INSERT INTO Customers (phone_num, name) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (phone_num, name))
                mysql.connection.commit()
            elif email == "":
                query = "INSERT INTO Customers (phone_num, name, visit_frequency_monthly) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (phone_num, name, visit_frequency_monthly))
                mysql.connection.commit()
            elif visit_frequency_monthly == "":
                query = "INSERT INTO Customers (phone_num, email, name) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (phone_num, email, name))
                mysql.connection.commit()
            else:
                query = "INSERT INTO Customers (phone_num, email, name, visit_frequency_monthly) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (phone_num, email, name, visit_frequency_monthly))
                mysql.connection.commit()

        return redirect("/customers")
        
# Delete Customers Page
@app.route('/delete_customers/<int:customer_id>')
def delete_customers(customer_id):
    query = "DELETE FROM Customers WHERE customer_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (customer_id,))
    mysql.connection.commit()

    return redirect("/customers")

# Update Customers Page
@app.route("/edit_customers/<int:customer_id>", methods=["POST", "GET"])
def edit_customers(customer_id):
    if request.method == "GET":
        query = "SELECT * FROM Customers WHERE customer_id = %s" #% (customer_id,) ###
        cur = mysql.connection.cursor()
        cur.execute(query, (customer_id,))
        data = cur.fetchone()
        
        return render_template("edit_customers.jinja", customers=data)
    
    if request.method == "POST":
        if request.form.get("edit_customer"):
            customer_id = request.form["customer_id"]
            phone_num = request.form["phone_num"]
            email = request.form["email"]
            name = request.form["name"]
            visit_frequency_monthly = request.form["visit_frequency_monthly"]

            if email == "" and visit_frequency_monthly == "":
                query = "UPDATE Customers SET Customers.phone_num = %s, Customers.email = NULL, Customers.name = %s, Customers.visit_frequency_monthly = NULL WHERE Customers.customer_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (phone_num, name, customer_id))
                mysql.connection.commit()
            elif email == "":
                query = "UPDATE Customers SET Customers.phone_num = %s, Customers.email = NULL, Customers.name = %s, Customers.visit_frequency_monthly = %s WHERE Customers.customer_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (phone_num, name, visit_frequency_monthly, customer_id))
                mysql.connection.commit()
            elif visit_frequency_monthly == "":
                query = "UPDATE Customers SET Customers.phone_num = %s, Customers.email = %s, Customers.name = %s, Customers.visit_frequency_monthly = NULL WHERE Customers.customer_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (phone_num, email, name, customer_id))
                mysql.connection.commit()
            else:
                query = "UPDATE Customers SET Customers.phone_num = %s, Customers.email = %s, Customers.name = %s, Customers.visit_frequency_monthly = %s WHERE Customers.customer_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (phone_num, email, name, visit_frequency_monthly, customer_id))
                mysql.connection.commit()
                cur.close()

        return redirect("/customers")


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    app.run(port=port, debug=True)  # Change port later