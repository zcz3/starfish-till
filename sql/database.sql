
-- SQL needed to create all the tables in the database.

CREATE TABLE IF NOT EXISTS products (
	id		INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	barcode		VARCHAR(100),
	name		VARCHAR(100) NOT NULL,
	price		DECIMAL(10,2) NOT NULL,
	vat_id		INT NOT NULL,
	vat		DECIMAL(10,2) NOT NULL,
	category_id	INT,
	stock		INT,
	stock_warning_level	INT,
	available	BIT(1),
	image		BLOB
);

CREATE TABLE IF NOT EXISTS categories (
	id		INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	name		VARCHAR(11) NOT NULL,
	image		BLOB
);

CREATE TABLE IF NOT EXISTS vat (
	id		INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	name		VARCHAR(100) NOT NULL,
	rate		DECIMAL(3,1) NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
	id		INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	title		VARCHAR(100),
	name		VARCHAR(20) NOT NULL,
	password	VARCHAR(40),
	role		INT
);

CREATE TABLE IF NOT EXISTS sales (
	id		INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	receipt_number	VARCHAR(10) NOT NULL,
	total		DECIMAL(10,2) NOT NULL,
	vat		DECIMAL(10,2) NOT NULL,
	date		DATETIME NOT NULL,
	user_id		INT,
	location_id	INT,
	payment_method	INT,
	cash_paid	DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS sale_items (
	id		INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	sale_id		INT NOT NULL,
	product_id	INT,
	name		VARCHAR(100),
	barcode		VARCHAR(100),
	price_each	DECIMAL(10,2) NOT NULL,
	vat_each	DECIMAL(10,2) NOT NULL,
	quantity	INT NOT NULL,
	total_price	DECIMAL(10,2) NOT NULL,
	total_vat	DECIMAL(10,2) NOT NULL,
	is_discount	BIT(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS locations (
	id		INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	name		VARCHAR(100) NOT NULL
);

