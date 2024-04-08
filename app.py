from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="space_bar",
    user="postgres",
    password="Password123",
    host="localhost",
    port="5432"
)

# Create a cursor object
cur = conn.cursor()

### ROUTE ::: ALL DRINKS ###
@app.route('/drinks', methods=['GET'])
def get_all_drinks():
    # Query the "drinks" table to get all data
    cur.execute("SELECT * FROM drinks")
    drinks = cur.fetchall()

    # Convert the query results to a list of dictionaries
    drink_list = []
    for drink in drinks:
        drink_dict = {
            'drink_id': drink[0],
            'drink_name': drink[1],
            'description': drink[2],
            'price': drink[3],
            'drink_type': drink[4],
            'ingredients': drink[5]
        }
        drink_list.append(drink_dict)

    return jsonify(drink_list)


### ROUTE ::: COCKTAILS ###
@app.route('/cocktails', methods=['GET'])
def get_cocktails():
    # Query the "drinks" table for drinks with a drink_type of 'cocktail'
    cur.execute("SELECT * FROM drinks WHERE drink_type = 'cocktail'")
    cocktails = cur.fetchall()

    # Convert the query results to a list of dictionaries
    cocktail_list = []
    for cocktail in cocktails:
        cocktail_dict = {
            'drink_id': cocktail[0],
            'drink_name': cocktail[1],
            'description': cocktail[2],
            'price': cocktail[3],
            'drink_type': cocktail[4],
            'ingredients': cocktail[5]
        }
        cocktail_list.append(cocktail_dict)

    return jsonify(cocktail_list)


# DO NOT TOUCH
if __name__ == '__main__':
    app.run(debug=True)