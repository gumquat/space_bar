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

# Open the JSON file and load the data
with open('drinks.json', 'r') as f:
    data = json.load(f)

# Insert the data into the 'drinks' table
for drink in data:
    sql = "INSERT INTO drinks (drink_id, drink_name, description, price, drink_type, ingredients) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (
        drink['drink_id'],
        drink['drink_name'],
        drink['description'],
        drink['price'],
        drink['drink_type'],
        drink['ingredients']
    )
    cur.execute(sql, values)

# Commit the changes and close the connection
conn.commit()
conn.close()