import psycopg2
import json

# PostgreSQL connection details
host = "your_host"
database = "your_database"
user = "your_username"
password = "your_password"

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password
)

# Create a cursor object
cur = conn.cursor()

# Open the JSON file
with open('drinks.json', 'r') as f:
    # Load the JSON data
    drinks_data = json.load(f)

# Create the table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS drinks (
        id SERIAL PRIMARY KEY,
        name TEXT,
        description TEXT,
        price FLOAT
    )
""")

# Insert the JSON data into the table
for drink in drinks_data:
    cur.execute("""
        INSERT INTO drinks (name, description, price)
        VALUES (%s, %s, %s)
    """, (drink['name'], drink['description'], drink['price']))

# Commit the changes and close the connection
conn.commit()
conn.close()