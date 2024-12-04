-- Team 40 ( Manuel Ramirez & Gabriel Del Valle Rivera )

-- Citation for the following code:
-- Date: 12/09/2024
-- Adapted from and based on:
-- Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app?tab=readme-ov-file#step-5---connecting-the-database
-- Source URL: https://www.w3schools.com/sql/default.asp

-- Disables commits and foreign key checks per recommendations
SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

-- Creates Customers table
DROP TABLE IF EXISTS Customers;

CREATE TABLE Customers (
    customer_id INT NOT NULL AUTO_INCREMENT,
    phone_num VARCHAR(10) NOT NULL,
    email VARCHAR(75),
    name VARCHAR(75) NOT NULL,
    visit_frequency_monthly INT,
    PRIMARY KEY (customer_id)
);
-- Inserts sample data into Customers
INSERT INTO Customers (phone_num, email, name, visit_frequency_monthly)
VALUES ('7561485213', 'gsmith@email.com', 'George Smith', 2),
('5413247813', 'asmith@gmail.com', 'Adam Smith', 1),
('4512369756', 'csmith@gmail.com', 'Charles Smith', 3);


-- Creates Producers table
DROP TABLE IF EXISTS Producers;

CREATE TABLE Producers (
    producer_id INT NOT NULL AUTO_INCREMENT,
    producer_name VARCHAR(50) NOT NULL,
    region VARCHAR(75) NOT NULL,
    region_details TEXT NOT NULL,
    PRIMARY KEY (producer_id)
);
-- Inserts sample data into Producers
INSERT INTO Producers (producer_name, region, region_details)
VALUES ('Bit Farms', 'Napa Valley', 'Producing wine since 1968'),
('Byte Farms', 'Sonoma', 'Producing wine since 1985'),
('Data Farms', 'Columbia Valley', 'Producing wine since 1928');


-- Creates Bottles table
DROP TABLE IF EXISTS Bottles;

CREATE TABLE Bottles (
    bottle_id INT NOT NULL AUTO_INCREMENT,
    bottle_name VARCHAR(50) NOT NULL,
    type VARCHAR(40) NOT NULL,
    volume INT NOT NULL,
    production_yr INT NOT NULL,
    alc_percent DECIMAL(4, 2) NOT NULL,
    price DECIMAL(7, 2) NOT NULL,
    producer_id INT NOT NULL,
    PRIMARY KEY (bottle_id),
    FOREIGN KEY (producer_id) REFERENCES Producers(producer_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
-- Inserts sample data into Bottles
INSERT INTO Bottles (bottle_name, type, volume, production_yr, alc_percent, price, producer_id)
VALUES ('Binary Blend', 'Merlot', 750, 2018, 12.00, 26.99, 1),
('Bitwise Bordeaux', 'Bordeaux', 750, 2020, 10.00, 32.99, 2),
('Compiler Cabernet', 'Cabernet', 750, 2015, 8.00, 45.99, 3);

-- Creates Orders table
DROP TABLE IF EXISTS Orders;

CREATE TABLE Orders (
    order_id INT NOT NULL AUTO_INCREMENT,
    customer_id INT,
    bottle_id INT NOT NULL,
    order_total DECIMAL(7, 2),
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (bottle_id) REFERENCES Bottles(bottle_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);
-- Inserts sample data into Orders
INSERT INTO Orders (customer_id, bottle_id, order_total)
VALUES (1, 3, 45.99),
(2, 2, 32.99),
(3, 1, 26.99);

-- Creates BottleOrders Table
DROP TABLE IF EXISTS BottleOrders;

CREATE TABLE BottleOrders (
	bottle_orderID INT NOT NULL AUTO_INCREMENT,
    order_id INT NOT NULL,
    bottle_id INT NOT NULL,
    order_qty INT NOT NULL,
    PRIMARY KEY (bottle_orderID),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
		ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (bottle_id) REFERENCES Bottles(bottle_id)
		ON UPDATE CASCADE ON DELETE CASCADE
);

-- Inserts sample data into BottleOrders
INSERT INTO BottleOrders (order_id, bottle_id, order_qty)
	VALUES (1, 3, 1),
	(2, 2, 1),
    (3, 1, 1);
    

-- Turns on commits and foreign key checks
SET FOREIGN_KEY_CHECKS=1;
COMMIT;