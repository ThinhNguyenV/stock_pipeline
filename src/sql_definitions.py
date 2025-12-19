# --- Database Connection Info (Dùng cho Postgres) ---

# --- DDL: Create Raw Stock Data Table ---
CREATE_RAW_STOCK_TABLE = """
CREATE TABLE IF NOT EXISTS raw_stock_data (
    "Date" TIMESTAMP NOT NULL,      
    "Ticker" TEXT NOT NULL,
    "Open" DOUBLE PRECISION,        
    "High" DOUBLE PRECISION,
    "Low" DOUBLE PRECISION,
    "Close" DOUBLE PRECISION,
    "Volume" BIGINT,              
    PRIMARY KEY ("Date", "Ticker")
);
"""

# --- DDL: Create Analyzed Stock Data Table ---
CREATE_ANALYZED_STOCK_TABLE = """
CREATE TABLE IF NOT EXISTS analyzed_stock_data (
    "Date" TIMESTAMP NOT NULL,
    "Ticker" TEXT NOT NULL,
    "Close" DOUBLE PRECISION,
    "SMA_50" DOUBLE PRECISION,
    "SMA_200" DOUBLE PRECISION,
    "Load_Timestamp" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("Date", "Ticker")
);
"""

ALL_CREATE_QUERIES = [
    CREATE_RAW_STOCK_TABLE,
    CREATE_ANALYZED_STOCK_TABLE
]

# --- DML: Insert Raw Data ---
INSERT_RAW_STOCK_DATA = """
INSERT INTO raw_stock_data ("Date", "Ticker", "Open", "High", "Low", "Close", "Volume")
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT ("Date", "Ticker") 
DO UPDATE SET 
    "Open" = EXCLUDED."Open",
    "High" = EXCLUDED."High",
    "Low" = EXCLUDED."Low",
    "Close" = EXCLUDED."Close",
    "Volume" = EXCLUDED."Volume";
"""

# --- DML: Insert Analyzed Data ---
INSERT_ANALYZED_STOCK_DATA = """
INSERT INTO analyzed_stock_data ("Date", "Ticker", "Close", "SMA_50", "SMA_200", "Load_Timestamp")
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT ("Date", "Ticker") 
DO UPDATE SET 
    "Close" = EXCLUDED."Close",
    "SMA_50" = EXCLUDED."SMA_50",
    "SMA_200" = EXCLUDED."SMA_200",
    "Load_Timestamp" = EXCLUDED."Load_Timestamp";
"""

# --- DML: Select Raw Data for Transformation ---
SELECT_RAW_STOCK_DATA = """
SELECT * FROM raw_stock_data WHERE "Ticker" = %s ORDER BY "Date" ASC;
"""