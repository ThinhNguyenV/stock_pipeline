# --- Database Initialization Queries ---

CREATE_RAW_TRANSACTIONS_TABLE = """
CREATE TABLE IF NOT EXISTS raw_transactions (
    transaction_id TEXT PRIMARY KEY,
    user_id TEXT,
    product_id TEXT,
    quantity INTEGER,
    price REAL,
    timestamp TIMESTAMP -- Postgres dùng TIMESTAMP thay vì TEXT cho thời gian
);
"""

CREATE_DIM_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS dim_users (
    user_key SERIAL PRIMARY KEY, -- SERIAL thay cho INTEGER PRIMARY KEY AUTOINCREMENT
    user_id TEXT UNIQUE,
    name TEXT,
    email TEXT,
    registration_date DATE
);
"""

CREATE_DIM_PRODUCTS_TABLE = """
CREATE TABLE IF NOT EXISTS dim_products (
    product_key SERIAL PRIMARY KEY, -- SERIAL thay cho AUTOINCREMENT
    product_id TEXT UNIQUE,
    name TEXT,
    category TEXT,
    unit_price REAL
);
"""

# --- Data Ingestion & Transformation Queries ---

# Postgres dùng %s thay vì ? làm placeholder
INSERT_RAW_TRANSACTION = """
INSERT INTO raw_transactions (transaction_id, user_id, product_id, quantity, price, timestamp)
VALUES (%s, %s, %s, %s, %s, %s);
"""

# Postgres dùng ON CONFLICT thay cho INSERT OR IGNORE
INSERT_DIM_USER = """
INSERT INTO dim_users (user_id, name, email, registration_date)
VALUES (%s, %s, %s, %s)
ON CONFLICT (user_id) DO NOTHING;
"""

INSERT_DIM_PRODUCT = """
INSERT INTO dim_products (product_id, name, category, unit_price)
VALUES (%s, %s, %s, %s)
ON CONFLICT (product_id) DO NOTHING;
"""

SELECT_USER_KEY = "SELECT user_key FROM dim_users WHERE user_id = %s"
SELECT_PRODUCT_KEY = "SELECT product_key FROM dim_products WHERE product_id = %s"