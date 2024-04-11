import psycopg2
import json
import os
import logging
import glob

LOG_FORMAT = "%(levelname)s %(asctime)s - %(name)s - %(message)s"
logging.basicConfig(filename='./logs/app.log',
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode='a')
logger = logging.getLogger('jsonLogger')

# Path to directory containing JSON files
json_dir_path = './datajsons/'

# Database connection parameters
dbname = os.environ.get("POSTGRES_DB")
user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
host = os.environ.get("DB_HOST")
port = os.environ.get("DB_PORT")

# Connect to the PostgreSQL database
conn = None
try:
    with psycopg2.connect(dbname=dbname, user=user, password=password,
                          host=host, port=port) as conn:
        with conn.cursor() as cur:
            # Glob pattern to match all .json files in json_dir_path
            for json_file_path in glob.glob(
                os.path.join(json_dir_path, '*.json')
            ):
                with open(json_file_path, 'r') as f:
                    drinks_data = json.load(f)

                for drink in drinks_data:
                    # Prepare data for insertion
                    values = (
                        drink['drink_name'],
                        drink['description'],
                        str(drink['price']),
                        drink['drink_type'],
                        drink['ingredients']
                    )

                    # SQL command
                    insert_sql = '''
                    INSERT INTO drinks
                    (drink_name, description, price, drink_type, ingredients)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (drink_name) DO NOTHING
                    '''

                    # Execute SQL command
                    try:
                        cur.execute(insert_sql, values)
                    except psycopg2.Error as e:
                        logger.error(f"Error inserting {values}: {e}")
                        continue  # Skip to the next record on error

                conn.commit()
                logger.info(
                    "Successfully inserted data into the drinks table."
                )
except psycopg2.OperationalError as e:
    logger.critical(f"Failed to connect to the database: {e}")
    raise e

# Commit the changes and close the connection
conn.commit()
conn.close()
