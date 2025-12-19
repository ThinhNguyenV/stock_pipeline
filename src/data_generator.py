import json
import uuid
import random
from datetime import datetime, timedelta
from faker import Faker

# Initialize Faker
fake = Faker()

# Configuration
NUM_TRANSACTIONS = 100
NUM_UNIQUE_USERS = 50
NUM_UNIQUE_PRODUCTS = 20
OUTPUT_FILE = "data/raw/transactions_{}.json".format(datetime.now().strftime("%Y%m%d%H%M%S"))

# Pre-generate unique user and product data
def generate_master_data():
    users = []
    for _ in range(NUM_UNIQUE_USERS):
        users.append({
            "user_id": str(uuid.uuid4()),
            "name": fake.name(),
            "email": fake.email(),
            "registration_date": (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat()
        })

    products = []
    categories = ["Electronics", "Books", "Clothing", "Home Goods", "Groceries"]
    for _ in range(NUM_UNIQUE_PRODUCTS):
        price = round(random.uniform(5.0, 500.0), 2)
        products.append({
            "product_id": str(uuid.uuid4()),
            "name": fake.word().capitalize() + " " + fake.word().capitalize(),
            "category": random.choice(categories),
            "unit_price": price
        })
    return users, products

# Generate transaction data
def generate_transactions(users, products):
    transactions = []
    start_time = datetime.now() - timedelta(hours=1)
    
    for i in range(NUM_TRANSACTIONS):
        # Select a random user and product
        user = random.choice(users)
        product = random.choice(products)
        
        # Simulate a timestamp within the last hour
        timestamp = (start_time + timedelta(seconds=i * (3600 / NUM_TRANSACTIONS))).isoformat()
        
        quantity = random.randint(1, 5)
        price = product["unit_price"]
        total_amount = round(quantity * price, 2)
        
        transaction = {
            "transaction_id": str(uuid.uuid4()),
            "user_id": user["user_id"],
            "product_id": product["product_id"],
            "quantity": quantity,
            "price": price, # Price here is the unit price from the product master data
            "total_amount": total_amount,
            "timestamp": timestamp,
            # Include master data for simplicity in this junior project
            "user_details": user,
            "product_details": product
        }
        transactions.append(transaction)
        
    return transactions

def main():
    print("Generating master data...")
    users, products = generate_master_data()
    
    print(f"Generating {NUM_TRANSACTIONS} transactions...")
    transactions = generate_transactions(users, products)
    
    print(f"Writing data to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(transactions, f, indent=4)
        
    print("Data generation complete.")
    print(f"File saved: {OUTPUT_FILE}")
    
    # Return the path for the next step in the pipeline
    return OUTPUT_FILE

if __name__ == "__main__":
    main()
