import psycopg2
from psycopg2 import sql
import os
import logging
from dotenv import load_dotenv

LOG_FORMAT = "%(levelname)s %(asctime)s - %(name)s - %(message)s"
logging.basicConfig(filename='./logs/app.log',
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode='a')
logger = logging.getLogger('tableLogger')


# /var/lib/postgresql/14/main


load_dotenv()


# Connect to the PostgreSQL database
conn = None
try:
    # Connect to the PostgreSQL database using context manager
    with psycopg2.connect(
        dbname=os.environ.get("POSTGRES_DB"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT")
    ) as conn:
        with conn.cursor() as cur:
            # Execute your SQL command
            the_big_query = '''
            CREATE TABLE IF NOT EXISTS "drinks" (
                "drink_id" SERIAL PRIMARY KEY,
                "drink_name" varchar UNIQUE,
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
            logger.info("Successfully created tables.")
except psycopg2.OperationalError as e:
    logger.critical(f"Failed to connect to the database: {e}")
    raise e

# CLOSE IT ALL OUT
cur.close()
conn.close()
