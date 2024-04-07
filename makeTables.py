# import pandas as pandas
import csv
import psycopg2
from psycopg2 import sql

#/var/lib/postgresql/14/main

    # CONNECT TO DATBASE
conn = psycopg2.connect(
    dbname="space_bar",
    user="postgres",
    password="Password123",
    host="localhost",
    port="5432"
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
'''

cur.execute(the_big_query)
conn.commit()

    # CLOSE IT ALL OUT
cur.close()
conn.close()