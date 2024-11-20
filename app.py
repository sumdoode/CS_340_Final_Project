from flask import Flask, render_template, json, redirect
import database.db_connector as db
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

db_connection = db.connect_to_database()

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "winery_db"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


# Routes

# Home Page
@app.route('/')
def root():
    return render_template("main.jinja")

# Customers Main Page
@app.route('/customers', methods=["POST", "GET"])
def customers():
    if request.method == "GET":
        query = "SELECT * FROM Customers"
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()

        return render_template('customers.jinja', customers=results)
    
    if request.method == "POST":
        if request.form.get("add_customer"):
            phone_num = request.form["phone_num"]
            email = request.form["email"]
            name = request.form["name"]
            visit_frequency_monthly = request.form["visit_frequency_monthly"]

            if email == "" and visit_frequency_monthly == "":
                query = "INSERT INTO Customers (phone_num, name) VALUES (%s, %s)"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(phone_num, name))
            elif email == "":
                query = "INSERT INTO Customers (phone_num, name, visit_frequency_monthly) VALUES (%s, %s, %d)"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(phone_num, name, visit_frequency_monthly))
            elif visit_frequency_monthly == "":
                query = "INSERT INTO Customers (phone_num, email, name) VALUES (%s, %s, %s)"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(phone_num, email, name))
            else:
                query = "INSERT INTO Customers (phone_num, email, name, visit_frequency_monthly) VALUES (%s, %s, %s)"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(phone_num, email, name, visit_frequency_monthly))

            return redirect("/customers")
        
# Delete Customers Page
@app.route('/delete_customer/<int:customer_id>')
def delete_customer(customer_id):
    query = "DELETE FROM Customers WHERE customer_id = '%s';"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(customer_id,))

    return redirect("/customers")

# Update Customers Page
@app.route("/edit_customers/<int:customer_id>", methods=["POST", "GET"])
def edit_customers(customer_id):
    if request.method == "GET":
        query = "SELECT * FROM Customers WHERE customer_id = %s" % (customer_id) ###
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()
        
        return render_template("edit_customers.jinja", data=data)
    
    if request.method == "POST":
        if request.form.get("edit_customer"):
            customer_id = request.form["customer_id"]
            phone_num = request.form["phone_num"]
            email = request.form["email"]
            name = request.form["name"]
            visit_frequency_monthly = request.form["visit_frequency_monthly"]

            if email == "" and visit_frequency_monthly == "":
                query = "UPDATE Customers SET Customers.phone_num = %s, Customers.email = NULL, Customers.name = %s, Customer.visit_frequency_monthly = NULL"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(phone_num, name))
            elif email == "":
                query = "UPDATE Customers SET Customers.phone_num = %s, Customers.email = NULL, Customers.name = %s, Customer.visit_frequency_monthly = %d"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(phone_num, name, visit_frequency_monthly))
            elif visit_frequency_monthly == "":
                query = "UPDATE Customers SET Customers.phone_num = %s, Customers.email = %s, Customers.name = %s, Customer.visit_frequency_monthly = NULL"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(phone_num, email, name))
            else:
                query = "UPDATE Customers SET Customers.phone_num = %s, Customers.email = %s, Customers.name = %s, Customer.visit_frequency_monthly = %s"
                cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(phone_num, email, name, visit_frequency_monthly))

            return redirect("/customers")


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    app.run(port=port, debug=True)  # Change port later