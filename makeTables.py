# import pandas as pandas
import csv
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

#/var/lib/postgresql/14/main
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
# Create a cursor object to execute SQL queries
cur = conn.cursor()

### MAKE A TON OF TABLES ALL AT ONCE
the_big_query = '''
CREATE TABLE "drinks" (
    "drink_id" SERIAL PRIMARY KEY,
    "drink_name" varchar,
    "description" varchar,
    "price" varchar,
    "drink_type" varchar,
    "ingredients" varchar[]
);

CREATE TABLE "users" (
    "user_id" SERIAL PRIMARY KEY,
    "username" varchar UNIQUE NOT NULL,
    "password" varchar NOT NULL,
    "email" varchar UNIQUE NOT NULL
);
'''

cur.execute(the_big_query)
conn.commit()

    # CLOSE IT ALL OUT
cur.close()
conn.close()