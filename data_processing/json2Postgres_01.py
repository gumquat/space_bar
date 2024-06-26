import psycopg2
import json
import os
import csv
import logging
import glob
from dotenv import load_dotenv
from fuzzywuzzy import process

load_dotenv()

LOG_FORMAT = "%(levelname)s %(asctime)s - %(name)s - %(message)s"
logging.basicConfig(filename='../logs/app.log',
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode='a')
logger = logging.getLogger('jsonLogger')

# Path to directory containing JSON files
json_dir_path = '../datajsons/'

# Database connection parameters
dbname = os.environ.get("POSTGRES_DB")
user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
host = os.environ.get("DB_HOST")
port = os.environ.get("DB_PORT")

def read_image_data(csv_file):
    image_data = {}
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            image_data[row['drink_name']] = row['drink_image_url']
    return image_data

image_data = read_image_data('../datajsons/drink_images.csv')

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
                    cur.execute(
                        "SELECT 1 FROM drinks WHERE drink_name = %s",
                        (drink['drink_name'],)
                    )
                    if cur.fetchone():
                        logger.info(f"Drink '{drink['drink_name']}' "
                                    f"already exists. Skipping.")
                        continue
                    
                    # Find the closest match for the drink name
                    best_match, score = process.extractOne(drink['drink_name'], image_data.keys())
                    if score > 80:
                        drink['image_url'] = image_data[best_match]
                    else:
                        logger.warning(f"Could not find image for {drink['drink_name']}")

                    # Prepare data for insertion
                    values = (
                        drink['drink_name'],
                        drink['description'],
                        str(drink['price']),
                        drink['drink_type'],
                        drink['ingredients'],
                        drink['image_url']
                    )

                    # SQL command
                    insert_sql = '''
                    INSERT INTO drinks
                    (drink_name, description, price, drink_type, ingredients, image_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
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
                    + json_file_path
                )
except psycopg2.OperationalError as e:
    logger.critical(f"Failed to connect to the database: {e}")
    raise e


# Commit the changes and close the connection
conn.commit()
conn.close()
