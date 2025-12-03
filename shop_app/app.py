# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
import psycopg2.extras


# Flask setup
app = Flask(__name__)
app.secret_key = "dev-secret-key-change-me"  # needed for flash() messages


# Database config
DB_CONFIG = {
    "dbname": "abdullahalghabban",  # same as $USER
    "user": "abdullahalghabban",    # or a dedicated user like 'shopapp'
    "password": "",                 # set if you created a password
    "host": "localhost",
    "port": 8888
}


def get_conn():
    """Open a new PostgreSQL connection."""
    return psycopg2.connect(**DB_CONFIG)


# Home
@app.route("/")
def index():
    return render_template("index.html")



# Products (SELECT + INSERT + DELETE)
@app.route("/products")
def products():
    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # Existing query: products
        cur.execute("""
            SELECT product_id, product_name, category, stock_quantity, cost,
                   supplier_id
            FROM shop.product
            ORDER BY product_id;
        """)
        rows = cur.fetchall()

        cur.execute("""
            SELECT supplier_id, supplier_name
            FROM shop.supplier
            ORDER BY supplier_id;
        """)
        suppliers = cur.fetchall()

    return render_template("products.html", products=rows, suppliers=suppliers)

@app.route("/products/add", methods=["POST"])
def add_product():
    name = request.form.get("product_name")
    category = request.form.get("category")
    stock_quantity = request.form.get("stock_quantity")
    cost = request.form.get("cost")
    supplier_id = request.form.get("supplier_id") or None  # optional

    if not name:
        flash("Product name is required.", "error")
        return redirect(url_for("products"))

    # basic validation / conversion
    try:
        stock_quantity = int(stock_quantity) if stock_quantity else 0
    except ValueError:
        flash("Stock quantity must be an integer.", "error")
        return redirect(url_for("products"))

    try:
        cost = float(cost) if cost else 0.0
    except ValueError:
        flash("Cost must be a number.", "error")
        return redirect(url_for("products"))

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO shop.product
                (product_name, category, stock_quantity, cost, supplier_id)
            VALUES (%s, %s, %s, %s, %s);
        """, (name, category, stock_quantity, cost, supplier_id))
        conn.commit()

    flash("Product added successfully.", "success")
    return redirect(url_for("products"))

@app.route("/products/<int:product_id>/delete", methods=["POST"])
def delete_product(product_id):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM shop.product
            WHERE product_id = %s;
        """, (product_id,))
        conn.commit()

    flash(f"Product {product_id} deleted.", "success")
    return redirect(url_for("products"))

# Customers (SELECT + INSERT + DELETE)
@app.route("/customers")
def customers():
    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            SELECT customer_id, first_name, last_name, email, phone_number,
                   street, city, state, zip
            FROM shop.customer
            ORDER BY customer_id;
        """)
        customers = cur.fetchall()
    return render_template("customers.html", customers=customers)


@app.route("/customers/add", methods=["POST"])
def add_customer():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    phone = request.form.get("phone_number")
    street = request.form.get("street")
    city = request.form.get("city")
    state = request.form.get("state")
    zip_code = request.form.get("zip")

    if not first_name or not last_name:
        flash("First name and last name are required.", "error")
        return redirect(url_for("customers"))

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO shop.customer
                (first_name, last_name, email, phone_number,
                 street, city, state, zip)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
        """, (first_name, last_name, email, phone, street, city, state, zip_code))
        conn.commit()

    flash("Customer added successfully.", "success")
    return redirect(url_for("customers"))


@app.route("/customers/<int:customer_id>/delete", methods=["POST"])
def delete_customer(customer_id):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM shop.customer
            WHERE customer_id = %s;
        """, (customer_id,))
        conn.commit()

    flash(f"Customer {customer_id} deleted.", "success")
    return redirect(url_for("customers"))


# Employees (SELECT + INSERT + DELETE)
@app.route("/employees")
def employees():
    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            SELECT employee_id, first_name, last_name, position, hire_date
            FROM shop.employee
            ORDER BY employee_id;
        """)
        employees = cur.fetchall()
    return render_template("employees.html", employees=employees)


@app.route("/employees/add", methods=["POST"])
def add_employee():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    position = request.form.get("position")
    hire_date = request.form.get("hire_date")

    if not first_name or not last_name or not hire_date:
        flash("First name, last name, and hire date are required.", "error")
        return redirect(url_for("employees"))

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO shop.employee
                (first_name, last_name, position, hire_date)
            VALUES (%s,%s,%s,%s);
        """, (first_name, last_name, position, hire_date))
        conn.commit()

    flash("Employee added successfully.", "success")
    return redirect(url_for("employees"))


@app.route("/employees/<int:employee_id>/delete", methods=["POST"])
def delete_employee(employee_id):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM shop.employee
            WHERE employee_id = %s;
        """, (employee_id,))
        conn.commit()

    flash(f"Employee {employee_id} deleted.", "success")
    return redirect(url_for("employees"))


# Suppliers (SELECT + INSERT + DELETE)
@app.route("/suppliers")
def suppliers():
    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            SELECT supplier_id, supplier_name, phone_number
            FROM shop.supplier
            ORDER BY supplier_id;
        """)
        suppliers = cur.fetchall()
    return render_template("suppliers.html", suppliers=suppliers)


@app.route("/suppliers/add", methods=["POST"])
def add_supplier():
    supplier_name = request.form.get("supplier_name")
    phone_number = request.form.get("phone_number")

    if not supplier_name:
        flash("Supplier name is required.", "error")
        return redirect(url_for("suppliers"))

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO shop.supplier (supplier_name, phone_number)
            VALUES (%s,%s);
        """, (supplier_name, phone_number))
        conn.commit()

    flash("Supplier added successfully.", "success")
    return redirect(url_for("suppliers"))


@app.route("/suppliers/<int:supplier_id>/delete", methods=["POST"])
def delete_supplier(supplier_id):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM shop.supplier
            WHERE supplier_id = %s;
        """, (supplier_id,))
        conn.commit()

    flash(f"Supplier {supplier_id} deleted.", "success")
    return redirect(url_for("suppliers"))


# Orders (SELECT + INSERT + UPDATE + DELETE)
@app.route("/orders")
def orders():
    """List all orders with basic info."""
    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            SELECT o.order_id,
                   o.order_date,
                   o.status,
                   o.payment_method,
                   o.total_amount,
                   c.first_name || ' ' || c.last_name AS customer_name
            FROM shop."order" o
            JOIN shop.customer c ON o.customer_id = c.customer_id
            ORDER BY o.order_id;
        """)
        orders = cur.fetchall()

        cur.execute("""
            SELECT customer_id, first_name || ' ' || last_name AS name
            FROM shop.customer
            ORDER BY customer_id;
        """)
        customers = cur.fetchall()

        cur.execute("""
            SELECT employee_id, first_name || ' ' || last_name AS name
            FROM shop.employee
            ORDER BY employee_id;
        """)
        employees = cur.fetchall()

    return render_template(
        "orders.html",
        orders=orders,
        customers=customers,
        employees=employees
    )


@app.route("/orders/add", methods=["POST"])
def add_order():
    """Create a new order (INSERT)."""
    order_date = request.form.get("order_date")  # e.g. 2025-10-24
    customer_id = request.form.get("customer_id")
    employee_id = request.form.get("employee_id") or None
    payment_method = request.form.get("payment_method") or "CASH"
    status = request.form.get("status") or "NEW"

    # for simplicity we’ll start with total_amount = 0;
    total_amount = 0

    if not customer_id:
        flash("Customer is required to create an order.", "error")
        return redirect(url_for("orders"))

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO shop."order"
                (order_date, status, payment_method, total_amount,
                 customer_id, employee_id)
            VALUES (%s,%s,%s,%s,%s,%s)
            RETURNING order_id;
        """, (order_date, status, payment_method, total_amount,
              customer_id, employee_id))
        new_id = cur.fetchone()[0]
        conn.commit()

    flash(f"Order {new_id} created.", "success")
    return redirect(url_for("order_detail", order_id=new_id))


@app.route("/orders/<int:order_id>")
def order_detail(order_id):
    """Show order info + its line items, and form to add a line."""
    with get_conn() as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # Order header
        cur.execute("""
            SELECT o.order_id,
                   o.order_date,
                   o.status,
                   o.payment_method,
                   o.total_amount,
                   c.first_name || ' ' || c.last_name AS customer_name,
                   o.customer_id,
                   o.employee_id
            FROM shop."order" o
            JOIN shop.customer c ON o.customer_id = c.customer_id
            WHERE o.order_id = %s;
        """, (order_id,))
        order = cur.fetchone()
        if not order:
            flash(f"Order {order_id} not found.", "error")
            return redirect(url_for("orders"))

        # Order lines
        cur.execute("""
            SELECT ol.order_id,
                   ol.product_id,
                   p.product_name,
                   ol.quantity,
                   ol.line_price
            FROM shop.order_line ol
            JOIN shop.product p ON ol.product_id = p.product_id
            WHERE ol.order_id = %s
            ORDER BY ol.product_id;
        """, (order_id,))
        lines = cur.fetchall()

        # Products for the dropdown
        cur.execute("""
            SELECT product_id, product_name, cost
            FROM shop.product
            ORDER BY product_id;
        """)
        products = cur.fetchall()

    return render_template(
        "order_detail.html",
        order=order,
        lines=lines,
        products=products
    )


@app.route("/orders/<int:order_id>/add_line", methods=["POST"])
def add_order_line(order_id):
    """Insert an order_line and update total_amount (INSERT + UPDATE)."""
    product_id = request.form.get("product_id")
    quantity = request.form.get("quantity")

    if not product_id or not quantity:
        flash("Product and quantity are required.", "error")
        return redirect(url_for("order_detail", order_id=order_id))

    quantity = int(quantity)

    with get_conn() as conn:
        cur = conn.cursor()

        # Get product cost
        cur.execute("""
            SELECT cost FROM shop.product
            WHERE product_id = %s;
        """, (product_id,))
        row = cur.fetchone()
        if not row:
            flash("Invalid product.", "error")
            return redirect(url_for("order_detail", order_id=order_id))
        cost = row[0]

        line_price = cost * quantity

        # Insert order line
        cur.execute("""
            INSERT INTO shop.order_line
                (order_id, product_id, quantity, line_price)
            VALUES (%s,%s,%s,%s);
        """, (order_id, product_id, quantity, line_price))

        # Update total_amount on the order
        cur.execute("""
            UPDATE shop."order"
            SET total_amount = total_amount + %s
            WHERE order_id = %s;
        """, (line_price, order_id))

        conn.commit()

    flash("Line item added.", "success")
    return redirect(url_for("order_detail", order_id=order_id))


@app.route("/orders/<int:order_id>/update_status", methods=["POST"])
def update_order_status(order_id):
    """Update order status (UPDATE)."""
    new_status = request.form.get("status")
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE shop."order"
            SET status = %s
            WHERE order_id = %s;
        """, (new_status, order_id))
        conn.commit()

    flash("Order status updated.", "success")
    return redirect(url_for("order_detail", order_id=order_id))


@app.route("/orders/<int:order_id>/delete", methods=["POST"])
def delete_order(order_id):
    """Delete an order and its lines (DELETE)."""
    with get_conn() as conn:
        cur = conn.cursor()
        # order_line has FK with ON DELETE CASCADE, but we can be explicit:
        cur.execute("DELETE FROM shop.order_line WHERE order_id = %s;", (order_id,))
        cur.execute('DELETE FROM shop."order" WHERE order_id = %s;', (order_id,))
        conn.commit()

    flash(f"Order {order_id} deleted.", "success")
    return redirect(url_for("orders"))


# Run
if __name__ == "__main__":
    app.run(debug=True)