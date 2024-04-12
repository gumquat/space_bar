import psycopg2
from psycopg2 import extras
import json
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

# Create a cursor object
cur = conn.cursor()

# Open the JSON file and load the data
with open('drinks.json', 'r') as f:
    drinks_data = json.load(f)

# Iterate through the data and insert into the "drinks" table
for drink in drinks_data:
    drink_name = drink['drink_name']
    description = drink['description']
    price = str(drink['price'])
    drink_type = drink['drink_type']
    ingredients = drink['ingredients']

    # Insert the data into the "drinks" table
    cur.execute(
        "INSERT INTO drinks (drink_name, description, price, drink_type, ingredients) "
        "VALUES (%s, %s, %s, %s, %s)",
        (drink_name, description, price, drink_type, ingredients)
    )

# Commit the changes and close the connection
conn.commit()
conn.close()