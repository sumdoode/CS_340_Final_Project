-- Team 40 ( Manuel Ramirez & Gabriel Del Valle Rivera )

-- Citation for the following code:
-- Date: 12/09/2024
-- Adapted from and based on:
-- Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file#step-5---connecting-the-database
-- Source URL: https://www.w3schools.com/sql/default.asp

-- Data Manipulation Queries


--           (READ queries)

-- Gets all customers to populate the Customers page
SELECT customer_id, name, phone_num, email, visit_frequency_monthly FROM Customers;

-- Gets all bottle information to populate Bottles page
SELECT bottle_id, bottle_name, type, volume, production_yr, alc_percent, price, producer_id FROM Bottles;

-- Gets all producer information to populate Producers page
SELECT producer_id, producer_name, region, region_details FROM Producers;

-- Gets all order information to populate Orders page
SELECT order_id, customer_id, bottle_id, order_total FROM Orders;

-- Gets all bottle orders to populate the Bottle Orders page
SELECT BottleOrders.bottle_orderID, Orders.order_id, Bottles.bottle_id, BottleOrders.order_qty FROM BottleOrders 
JOIN Orders on BottleOrders.order_id = Orders.order_id JOIN Bottles on BottleOrders.bottle_id = Bottles.bottle_id;


--           (CREATE queries)

-- Inserts a new customer into Customers table
INSERT INTO Customers (name, phone_num, email) VALUES (%s, %s, %s);

-- Inserts a new bottle into Bottles table
INSERT INTO Bottles (bottle_name, type, volume, production_yr, alc_percent, price, producer_id) VALUES (%s, %s, %d, %d, %f, %f, %d);

-- Inserts a new producer into Producers table
INSERT INTO Producers (producer_name, region, region_details) VALUES (%s, $s, $s);

-- Inserts a new order into the Orders table
INSERT INTO Orders (customer_id, bottle_id, order_total) VALUES (%d, %d, %f);

-- Inserts a new bottle order into BottleOrders table
INSERT INTO BottleOrders (order_id, bottle_id, order_qty) VALUES (%d, %d, %d);


--           (UPDATE queries)

-- Updates existing bottle in Bottles table
UPDATE Bottles SET Bottles.bottle_name = %s, Bottles.type = %s, Bottles.volume = %d, Bottles.production_yr = %d, Bottles.alc_percent = %f,
				   Bottles.price = %f, Bottles.producer_id = %d WHERE Customers.customer_id = %s;
                   
-- Updates existing producer in Producers table
UPDATE Producers SET Producers.producer_name = %s, Producers.region = %s, Producers.region_details = %s WHERE Customers.customer_id = %s;

-- Updates existing producer in Producers table if region_details is null
UPDATE Producers SET Producers.producer_name = %s, Producers.region = %s, Producers.region_details = NULL WHERE Customers.customer_id = %s;

-- Updates existing bottle order in BottleOrders table
UPDATE BottleOrders SET BottleOrders.order_qty = %d WHERE Orders.order_id= %s AND Bottles.bottle_id = %s;


--           (DELETE queries)

-- Deletes bottle from Bottles table
DELETE FROM Bottles WHERE bottle_id = '%s';

-- Deletes bottle order from BottleOrders table (M:M)
DELETE FROM BottleOrders WHERE order_id = '%d' AND bottle_id = '%d';


--           (Dropdown queries)

-- Select query for producers dropdown menu
SELECT producer_id, producer_name FROM Producers;
