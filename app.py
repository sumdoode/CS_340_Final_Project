# Citation for the following code:
# Date: 12/09/2024
# Adapted from and based on:
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file#step-5---connecting-the-database
# Source URL: https://flask.palletsprojects.com/en/stable/quickstart/
# Source URL: https://www.askpython.com/python-modules/flask/flask-crud-application


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
        # Query to display Customers table                             
        query = "SELECT * FROM Customers"                           
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template('customers.jinja', customers=data)
    
    # Manages form to add new customers
    if request.method == "POST":                                   
         if "add_customer" in request.form.keys():
            phone_num = request.form["phone_num"]
            email = request.form["email"]
            name = request.form["name"]
            visit_frequency_monthly = request.form["visit_frequency_monthly"]

            # Manages NULL email AND NULL visit freq case
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

# Handles route for editing an existing customer        
def edit_customers(customer_id):
    if request.method == "GET":
        query = "SELECT * FROM Customers WHERE customer_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (customer_id,))
        data = cur.fetchone()
        
        return render_template("edit_customers.jinja", customers=data)
    
    # Handles form submission of edited customer record and returns to customers page
    if request.method == "POST":                                                
        if "edit_customers" in request.form.keys():
            customer_id = request.form["customer_id"]
            phone_num = request.form["phone_num"]
            email = request.form["email"]
            name = request.form["name"]
            visit_frequency_monthly = request.form["visit_frequency_monthly"]

            # Handles NULL cases of email and visit freq
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

        # Query to display bottles AND producer name utilizing a JOIN
        query = "SELECT Bottles.*, Producers.producer_name FROM Bottles JOIN Producers on Bottles.producer_id = Producers.producer_id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Query to return producer names for dropdown menu
        query2 = "SELECT producer_id, producer_name FROM Producers"
        cur.execute(query2)
        producers = cur.fetchall()

        return render_template('bottles.jinja', bottles=data, producers=producers)
    
    # Handles adding a new bottle
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
                
            return redirect("/bottles")

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
        # Query to edit an existing bottle; displays producer name
        query = "SELECT Bottles.*, Producers.producer_name FROM Bottles JOIN Producers on Bottles.producer_id = Producers.producer_id WHERE Bottles.bottle_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (bottle_id,))
        data = cur.fetchone()

        # Query used to populate producer name in dropdown menu
        query2 = "SELECT producer_id, producer_name FROM Producers"
        cur.execute(query2)
        producers = cur.fetchall()
        
        return render_template("edit_bottles.jinja", bottles=data, producers=producers)
    
    # Submits updated bottle to the database
    if request.method == "POST":
        if "edit_bottles" in request.form.keys():
            bottle_id = request.form["bottle_id"]
            bottle_name = request.form["bottle_name"]
            type = request.form["type"]
            volume = request.form["volume"]
            production_yr = request.form["production_yr"]
            alc_percent = request.form["alc_percent"]
            price = request.form["price"]
            producer_id = request.form["producer_id"]

            query = "UPDATE Bottles SET bottle_name = %s, type = %s, volume = %s, production_yr = %s, alc_percent = %s, price = %s, producer_id = %s WHERE bottle_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (bottle_name, type, volume, production_yr, alc_percent, price, producer_id, bottle_id))
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
    
    # Handles adding a new producer
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

    # Handles showing producer to be edited
    if request.method == "GET":
        query = "SELECT * FROM Producers WHERE producer_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (producer_id,))
        data = cur.fetchone()
        
        return render_template("edit_producer.jinja", producers=data)
    
    # Handles sending data to update producer
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
        # Query to show orders table including customer and bottle names
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
    
    # Handles sending new order data
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
        # Query to fetch the order to edit
        query_order = "SELECT * FROM Orders WHERE order_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query_order, (order_id,))
        order = cur.fetchone()

        # Query to fetch all customers for dropdown
        query_customers = "SELECT customer_id, name FROM Customers"
        cur.execute(query_customers)
        customers = cur.fetchall()

        # Query to fetch all bottles for dropdown
        query_bottles = "SELECT bottle_id, bottle_name FROM Bottles"
        cur.execute(query_bottles)
        bottles = cur.fetchall()

        return render_template('edit_order.jinja', order=order, customers=customers, bottles=bottles)

    # Handles updating existing order data
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

# Bottle Orders Page
@app.route('/bottle_orders', methods=["POST", "GET"])
def bottle_orders():
    if request.method == "GET":
        # Query to fetch bottle orders with details
        query = """
            SELECT BottleOrders.bottle_orderID, Orders.order_id, Bottles.bottle_id, BottleOrders.order_qty
            FROM BottleOrders
            JOIN Orders ON BottleOrders.order_id = Orders.order_id
            LEFT JOIN Bottles ON BottleOrders.bottle_id = Bottles.bottle_id;
        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Query to get all orders
        query2 = "SELECT order_id FROM Orders"  
        cur.execute(query2)
        orders = cur.fetchall()

        # Query to get all bottles
        query3 = "SELECT bottle_id, bottle_name FROM Bottles"  
        cur.execute(query3)
        bottles = cur.fetchall()

        return render_template('bottle_orders.jinja', bottleorders=data, orders=orders, bottles=bottles)

    # Handles adding a new bottle order to th table
    if request.method == "POST":
        if "add_bottle_order" in request.form.keys(): 
            order_id = request.form["order_id"]
            bottle_id = request.form["bottle_id"]
            order_qty = request.form["order_qty"]

            # Handles a null bottle_id
            if not bottle_id:
                bottle_id = None

            # Insert new bottle order into BottleOrders table
            query = "INSERT INTO BottleOrders (order_id, bottle_id, order_qty) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (order_id, bottle_id, order_qty))
            mysql.connection.commit()
            cur.close()

            return redirect("/bottle_orders")


# Delete Bottle Orders Page
@app.route('/delete_bottle_order/<int:bottle_orderID>')
def delete_bottle_order(bottle_orderID):
    query = "DELETE FROM BottleOrders WHERE bottle_orderID = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (bottle_orderID,))
    mysql.connection.commit()
    cur.close()

    return redirect('/bottle_orders')


# Update Bottle Order
@app.route('/edit_bottle_orders/<int:bottle_orderID>', methods=["POST", "GET"])
def edit_bottle_orders(bottle_orderID):
    if request.method == "GET":
        # Fetch the existing bottle order data
        query = "SELECT * FROM BottleOrders WHERE bottle_orderID = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (bottle_orderID,))
        data = cur.fetchone()

        # Get available orders...
        cur.execute("SELECT order_id FROM Orders")
        orders = cur.fetchall()
        
        # ...and bottles for the form
        cur.execute("SELECT bottle_id, bottle_name FROM Bottles")
        bottles = cur.fetchall()

        return render_template('edit_bottle_orders.jinja', bottleorder=data, orders=orders, bottles=bottles)

    # Sends updated bottle order 
    if request.method == "POST":
         if "edit_bottle_order" in request.form.keys():
            order_id = request.form["order_id"]
            bottle_id = request.form["bottle_id"]
            order_qty = request.form["order_qty"]

            # Handles a null bottle_id
            if not bottle_id:
                bottle_id = None

            # Update the existing record in BottleOrders table
            query = "UPDATE BottleOrders SET order_id = %s, bottle_id = %s, order_qty = %s WHERE bottle_orderID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (order_id, bottle_id, order_qty, bottle_orderID))
            mysql.connection.commit()
            cur.close()

            return redirect("/bottle_orders")


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 53785))
    app.run(port=port, debug=True)  # Change port later