from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

# For local Testing
#app.config["MYSQL_HOST"] = "localhost"
#pp.config["MYSQL_USER"] = "root"
#app.config["MYSQL_PASSWORD"] = ""
#app.config["MYSQL_DB"] = "winery_db"
#app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# For OSU Servers
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_ramirman"
app.config["MYSQL_PASSWORD"] = "0125"
app.config["MYSQL_DB"] = "cs340_ramirman"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


# Home Page
@app.route('/')
def root():
    return render_template("main.jinja")

# ------------------------------------------------------------------------(CUSTOMERS ROUTES)----------------------------------------------------------------------------------#

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
         if "add_customer" in request.form.keys():
            phone_num = request.form["phone_num"]
            email = request.form["email"]
            name = request.form["name"]
            visit_frequency_monthly = request.form["visit_frequency_monthly"]

            if email == "" and visit_frequency_monthly == "":
                query = "INSERT INTO Customers (phone_num, name) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (phone_num, name))
                mysql.connection.commit()
                cur.close()
            elif email == "":
                query = "INSERT INTO Customers (phone_num, name, visit_frequency_monthly) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (phone_num, name, visit_frequency_monthly))
                mysql.connection.commit()
                cur.close()
            elif visit_frequency_monthly == "":
                query = "INSERT INTO Customers (phone_num, email, name) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (phone_num, email, name))
                mysql.connection.commit()
                cur.close()
            else:
                query = "INSERT INTO Customers (phone_num, email, name, visit_frequency_monthly) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (phone_num, email, name, visit_frequency_monthly))
                mysql.connection.commit()
                cur.close()
                
            return redirect("/customers")
        
# Delete Customers Page
@app.route('/delete_customers/<int:customer_id>')
def delete_customers(customer_id):
    query = "DELETE FROM Customers WHERE customer_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (customer_id,))
    mysql.connection.commit()
    cur.close()

    return redirect("/customers")

# Update Customers Page
@app.route("/edit_customers/<int:customer_id>", methods=["POST", "GET"])
def edit_customers(customer_id):
    if request.method == "GET":
        query = "SELECT * FROM Customers WHERE customer_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (customer_id,))
        data = cur.fetchone()
        
        return render_template("edit_customers.jinja", customers=data)
    
    if request.method == "POST":
        if "edit_customers" in request.form.keys():
            customer_id = request.form["customer_id"]
            phone_num = request.form["phone_num"]
            email = request.form["email"]
            name = request.form["name"]
            visit_frequency_monthly = request.form["visit_frequency_monthly"]

            if email == "" and visit_frequency_monthly == "":
                query = "UPDATE Customers SET phone_num = %s, email = NULL, name = %s, visit_frequency_monthly = NULL WHERE customer_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (phone_num, name, customer_id))
                mysql.connection.commit()
                cur.close()
            elif email == "":
                query = "UPDATE Customers SET phone_num = %s, email = NULL, name = %s, visit_frequency_monthly = %s WHERE customer_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (phone_num, name, visit_frequency_monthly, customer_id))
                mysql.connection.commit()
                cur.close()
            elif visit_frequency_monthly == "":
                query = "UPDATE Customers SET phone_num = %s, email = %s, name = %s, visit_frequency_monthly = NULL WHERE customer_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (phone_num, email, name, customer_id))
                mysql.connection.commit()
                cur.close()
            else:
                query = "UPDATE Customers SET phone_num = %s, email = %s, name = %s, visit_frequency_monthly = %s WHERE customer_id = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (phone_num, email, name, visit_frequency_monthly, customer_id))
                mysql.connection.commit()
                cur.close()
        
        return redirect("/customers")
    
# ------------------------------------------------------------------------(BOTTLES ROUTES)----------------------------------------------------------------------------------#

# Bottles Main Page
@app.route('/bottles', methods=["POST", "GET"])
def bottles():
    if request.method == "GET":
        query = "SELECT * FROM Bottles"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template('bottles.jinja', bottles=data)
    
    if request.method == "POST":
         if "add_bottle" in request.form.keys():
            bottle_name = request.form["bottle_name"]
            type = request.form["type"]
            volume = request.form["volume"]
            production_yr = request.form["production_yr"]
            alc_percent = request.form["alc_percent"]
            price = request.form["price"]
            producer_id = request.form["producer_id"]

            query = "INSERT INTO Bottles (bottle_name, type, volume, production_yr, alc_percent, price, producer_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (bottle_name, type, volume, production_yr, alc_percent, price, producer_id))
            mysql.connection.commit()
            cur.close()
                
            return redirect("/customers")

# Delete Bottles Page
@app.route('/delete_bottles/<int:bottle_id>')
def delete_bottles(bottle_id):
    query = "DELETE FROM Bottles WHERE bottle_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (bottle_id,))
    mysql.connection.commit()
    cur.close()

    return redirect("/bottles")

# Update Bottles Page
@app.route("/edit_bottles/<int:bottle_id>", methods=["POST", "GET"])
def edit_bottles(bottle_id):
    if request.method == "GET":
        query = "SELECT * FROM Bottles WHERE bottle_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (bottle_id,))
        data = cur.fetchone()
        
        return render_template("edit_bottles.jinja", bottles=data)
    
    if request.method == "POST":
        if "edit_bottles" in request.form.keys():
            bottle_id = request.form["bottle_id"]
            bottle_name = request.form["bottle_name"]
            type = request.form["type"]
            volume = request.form["volume"]
            production_yr = request.form["production_yr"]
            alc_percent = request.form["alc_percent"]
            price = request.form["price"]

            
            query = "UPDATE Bottles SET bottle_name = %s, type = %s, volume = %s, production_yr = %s, alc_percent = %s, price = %s WHERE bottle_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (bottle_name, type, volume, production_yr, alc_percent, price, bottle_id))
            mysql.connection.commit()
            cur.close()
        
            return redirect("/bottles")


# ----------------------------------------------------------------------------(PRODUCERS ROUTES)----------------------------------------------------------------------------------#

# Producers Main Page
@app.route('/producers', methods=["POST", "GET"])
def producers():
    if request.method == "GET":
        query = "SELECT * FROM Producers"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template('producers.jinja', producers=data)
    
    if request.method == "POST":
        if "add_producer" in request.form.keys():
            producer_name = request.form["producer_name"]
            region = request.form["region"]
            region_details = request.form["region_details"]

            query = "INSERT INTO Producers (producer_name, region, region_details) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (producer_name, region, region_details))
            mysql.connection.commit()
            cur.close()

            return redirect("/producers")


# Delete Producer Page
@app.route('/delete_producer/<int:producer_id>')
def delete_producer(producer_id):
    query = "DELETE FROM Producers WHERE producer_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (producer_id,))
    mysql.connection.commit()
    cur.close()

    return redirect("/producers")


# Update Producer Page
@app.route("/edit_producer/<int:producer_id>", methods=["POST", "GET"])
def edit_producer(producer_id):
    if request.method == "GET":
        query = "SELECT * FROM Producers WHERE producer_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (producer_id,))
        data = cur.fetchone()
        
        return render_template("edit_producer.jinja", producer=data)
    
    if request.method == "POST":
        if "edit_producer" in request.form.keys():
            producer_id = request.form["producer_id"]
            producer_name = request.form["producer_name"]
            region = request.form["region"]
            region_details = request.form["region_details"]

            query = "UPDATE Producers SET producer_name = %s, region = %s, region_details = %s WHERE producer_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (producer_name, region, region_details, producer_id))
            mysql.connection.commit()
            cur.close()

        return redirect("/producers")


# ----------------------------------------------------------------------------(ORDERS ROUTES)-------------------------------------------------------------------------------------#

# Orders Main Page
@app.route('/orders', methods=["POST", "GET"])
def orders():
    if request.method == "GET":
        query = """
        SELECT Orders.order_id, Orders.customer_id, Orders.bottle_id, Orders.order_total, Customers.name, Bottles.bottle_name
        FROM Orders
        JOIN Customers ON Orders.customer_id = Customers.customer_id
        JOIN Bottles ON Orders.bottle_id = Bottles.bottle_id;
        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

         # Query to fetch all customers for the dropdown
        query_customers = "SELECT customer_id, name FROM Customers"
        cur.execute(query_customers)
        customers = cur.fetchall()

        # Query to fetch all bottles for the dropdown
        query_bottles = "SELECT bottle_id, bottle_name FROM Bottles"
        cur.execute(query_bottles)
        bottles = cur.fetchall()

        return render_template('orders.jinja', orders=data, customers=customers, bottles=bottles)
    
    if request.method == "POST":
        if "add_order" in request.form.keys():
            customer_id = request.form["customer_id"]
            bottle_id = request.form["bottle_id"]
            order_total = request.form["order_total"]

            query = "INSERT INTO Orders (customer_id, bottle_id, order_total) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (customer_id, bottle_id, order_total))
            mysql.connection.commit()
            cur.close()

            return redirect("/orders")

# Delete Order Page
@app.route('/delete_order/<int:order_id>')
def delete_order(order_id):
    query = "DELETE FROM Orders WHERE order_id = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (order_id,))
    mysql.connection.commit()
    cur.close()

    return redirect("/orders")


# Update Order Page
@app.route("/edit_order/<int:order_id>", methods=["POST", "GET"])
def edit_order(order_id):
    if request.method == "GET":
        # Fetch the order to edit
        query_order = "SELECT * FROM Orders WHERE order_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query_order, (order_id,))
        order = cur.fetchone()

        # Fetch all customers for the form
        query_customers = "SELECT customer_id, name FROM Customers"
        cur.execute(query_customers)
        customers = cur.fetchall()

        # Fetch all bottles for the form
        query_bottles = "SELECT bottle_id, bottle_name FROM Bottles"
        cur.execute(query_bottles)
        bottles = cur.fetchall()

        # Render the edit order page
        return render_template('edit_order.jinja', order=order, customers=customers, bottles=bottles)

    if request.method == "POST":
        if "edit_order" in request.form.keys():
            order_id = request.form["order_id"]
            customer_id = request.form["customer_id"]
            bottle_id = request.form["bottle_id"]
            order_total = request.form["order_total"]

            query = "UPDATE Orders SET customer_id = %s, bottle_id = %s, order_total = %s WHERE order_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (customer_id, bottle_id, order_total, order_id))
            mysql.connection.commit()
            cur.close()

        return redirect("/orders")


# ------------------------------------------------------------------------(BOTTLE ORDERS ROUTES)----------------------------------------------------------------------------------#

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 53785))
    app.run(port=port, debug=True)  # Change port later