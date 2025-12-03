# CSE 412: Shop Management Application  
A Flask web application that interacts with a PostgreSQL database to manage a small retail shop.  
This project implements Phase 2 and Phase 3 requirements of the CSE 412 course, including:  
- ER → Relational schema (DDL)  
- Data population (CSV + COPY)  
- SQL CRUD operations  
- A functioning application UI backed by real SQL queries  

---

## Features
The application supports database-backed operations for:

### Products
- View all products  
- Display supplier relationship  

### Customers
- View customers  
- Add customers  
- Delete customers  

### Orders
- View all orders  
- Create new orders  
- Add order line items  
- Update order status  
- Delete orders  

### Schema Highlights
All tables live in schema **`shop`**:
- `supplier`
- `product`
- `customer`
- `employee`
- `"order"`
- `order_line`

---

## Setup Instructions

### 1. Install Dependencies
```bash
pip install flask psycopg2-binary
```

2. Start PostgreSQL (your local DB)
```bash
pg_ctl -D "$HOME/db412" -o '-k /tmp -p 8888' start
```
3. Create Database Schema
```bash
psql -d "$USER" -p 8888 -v ON_ERROR_STOP=1 -f _schema.sql
```
4. Load Data
Open psql:
```bash
psql -d "$USER" -p 8888
```
Run the COPY commands:
```SQL
SET search_path TO shop;

COPY shop.supplier (supplier_name, phone_number)
FROM '/absolute/path/suppliers.csv'
WITH (FORMAT csv, HEADER true);

COPY shop.product (product_name, category, stock_quantity, cost, supplier_id)
FROM '/absolute/path/products.csv'
WITH (FORMAT csv, HEADER true);

COPY shop.customer (first_name, last_name, email, phone_number, street, city, state, zip)
FROM '/absolute/path/customers.csv'
WITH (FORMAT csv, HEADER true);

COPY shop.employee (first_name, last_name, position, hire_date)
FROM '/absolute/path/employees.csv'
WITH (FORMAT csv, HEADER true);

COPY shop."order" (order_date, status, payment_method, total_amount, customer_id, employee_id)
FROM '/absolute/path/orders.csv'
WITH (FORMAT csv, HEADER true);

COPY shop.order_line (order_id, product_id, quantity, line_price)
FROM '/absolute/path/order_lines.csv'
WITH (FORMAT csv, HEADER true);
```
▶️ Running the App
From the project directory:
```bash
python app.py
```
Navigate to:

http://127.0.0.1:5000/

