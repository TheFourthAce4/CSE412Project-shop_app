DROP SCHEMA IF EXISTS shop CASCADE;
CREATE SCHEMA shop;
SET search_path = shop;

CREATE TABLE customer (
  customer_id      INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  first_name       VARCHAR(50) NOT NULL,
  last_name        VARCHAR(50) NOT NULL,
  email            VARCHAR(255) UNIQUE,
  phone_number     VARCHAR(25),
  -- composite Address attribute flattened
  street           VARCHAR(120),
  city             VARCHAR(80),
  state            VARCHAR(50),
  zip              VARCHAR(15)
);

CREATE TABLE employee (
  employee_id      INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  first_name       VARCHAR(50) NOT NULL,
  last_name        VARCHAR(50) NOT NULL,
  position         VARCHAR(80),
  hire_date        DATE NOT NULL
);

CREATE TABLE supplier (
  supplier_id      INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  supplier_name    VARCHAR(120) NOT NULL,
  phone_number     VARCHAR(25),
  CONSTRAINT uq_supplier_name UNIQUE (supplier_name)
);

CREATE TABLE product (
  product_id       INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  product_name     VARCHAR(120) NOT NULL,
  category         VARCHAR(80),
  stock_quantity   INT NOT NULL DEFAULT 0 CHECK (stock_quantity >= 0),
  cost             NUMERIC(12,2) NOT NULL CHECK (cost >= 0),
  supplier_id      INT NOT NULL,
  CONSTRAINT fk_product_supplier
    FOREIGN KEY (supplier_id)
    REFERENCES supplier(supplier_id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);

CREATE TABLE "order" (
  order_id         INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  order_date       TIMESTAMP NOT NULL DEFAULT NOW(),
  status           TEXT NOT NULL CHECK (status IN ('NEW','PAID','SHIPPED','CANCELLED')) DEFAULT 'NEW',
  payment_method   TEXT CHECK (payment_method IN ('CASH','CARD','TRANSFER','OTHER')),
  total_amount     NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (total_amount >= 0),
  customer_id      INT NOT NULL,
  employee_id      INT,
  CONSTRAINT fk_order_customer
    FOREIGN KEY (customer_id)
    REFERENCES customer(customer_id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT,
  CONSTRAINT fk_order_employee
    FOREIGN KEY (employee_id)
    REFERENCES employee(employee_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL
);

CREATE TABLE order_line (
  order_id         INT NOT NULL,
  product_id       INT NOT NULL,
  quantity         INT NOT NULL CHECK (quantity > 0),
  line_price       NUMERIC(12,2) NOT NULL CHECK (line_price >= 0),
  -- Composite PK = (order_id, product_id)
  PRIMARY KEY (order_id, product_id),
  CONSTRAINT fk_ol_order
    FOREIGN KEY (order_id)
    REFERENCES "order"(order_id)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
  CONSTRAINT fk_ol_product
    FOREIGN KEY (product_id)
    REFERENCES product(product_id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT
);