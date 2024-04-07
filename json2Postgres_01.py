import psycopg2
import json

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="space_bar",
    user="postgres",
    password="Password123",
    host="localhost",
    port="5432"
)

# Create a cursor object
cur = conn.cursor()

# Open the JSON file
with open('drinks.json', 'r') as f:
    # Load the JSON data
    drinks_data = json.load(f)

# Insert the JSON data into the table
# MAKE SURE THAT THE LAST %S imports AN ARRAY!!!!!!!!! <---
for drink in drinks_data:
    cur.execute("""
        INSERT INTO drinks (name, description, price, drink_type, ingredients)
        VALUES (%s, %s, %s, %s, %s) 
    """, (drink['name'], drink['description'], drink['price']))

# Commit the changes and close the connection
conn.commit()
conn.close()