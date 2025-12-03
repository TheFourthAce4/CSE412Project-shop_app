# CSE 412: Shop Management Application  
A Flask web application that interacts with a PostgreSQL database to manage a small retail shop.  
This project implements Phase 1, Phase 2, and Phase 3 requirements of the CSE 412 course, including:  
- ER → Relational schema (DDL)  
- Data population (CSV + COPY)  
- SQL CRUD operations  
- A functioning application UI backed by real SQL queries  

---

## Features
The application supports database-backed operations for:

Products
- View all products
- Add new products (name, category, stock, cost, supplier)
- Delete products
- Supplier dropdown populated dynamically

Customers
- View customers
- Add new customers
- Delete customers
- Capture full address & contact information

Employees
- View employees
- Add employees (first/last name, position, hire date)
- Delete employees

Suppliers
- View suppliers
- Add new supplier
- Delete suppliers

Orders
- Create new orders
- Add order line items
- Update order status (NEW, PAID, SHIPPED, CANCELLED)
- Auto-calculate total_amount
- Cascade delete lines + order

UI / UX
- Fully responsive using Bootstrap 5
- Modernized dashboard layout (card-style home page)
- Consistent layout and navigation across all pages
- Flash notifications for all actions (success/error)

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

1. Clone the repo
```bash
git clone <https://github.com/TheFourthAce4/CSE412Project-shop_app.git>
cd project
```
2. Configure PostgreSQL
Update these fields inside app.py:
```bash
   DB_CONFIG = {
    "dbname": "YOUR_DB_NAME",
    "user": "YOUR_DB_USER",
    "password": "",
    "host": "localhost",
    "port": 8888
}
```
3. Install required packages
```bash
pip install flask psycopg2-binary
```

4. Start PostgreSQL (your local DB)
```bash
pg_ctl -D "$HOME/db412" -o '-k /tmp -p 8888' start
```
5. Create Database Schema
```bash
psql -d "$USER" -p 8888 -v ON_ERROR_STOP=1 -f _schema.sql
```
6. Load Data
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
7. Run the App
From the project directory:
```bash
python app.py
```
Navigate to:

http://127.0.0.1:5000/

