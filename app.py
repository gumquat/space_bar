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
    cur.execute("SELECT * FROM drinks WHERE drink_type = 'Cocktail'")
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

### ROUTE ::: COCKTAILS ###
@app.route('/beers', methods=['GET'])
def get_beers():
    # Query the "drinks" table for drinks with a drink_type of 'beer'
    cur.execute("SELECT * FROM drinks WHERE drink_type = 'Beer'")
    beers = cur.fetchall()

    # Convert the query results to a list of dictionaries
    beer_list = []
    for beer in beers:
        beer_dict = {
            'drink_id': beer[0],
            'drink_name': beer[1],
            'description': beer[2],
            'price': beer[3],
            'drink_type': beer[4],
            #'ingredients': beer[5]
        }
        beer_list.append(beer_dict)

    return jsonify(beer_list)


### ROUTE ::: WINE ###
@app.route('/wines', methods=['GET'])
def get_wines():
    # Query the "drinks" table for drinks with a drink_type of 'wine'
    cur.execute("SELECT * FROM drinks WHERE drink_type = 'Wine'")
    wines = cur.fetchall()

    # Convert the query results to a list of dictionaries
    wine_list = []
    for wine in wines:
        wine_dict = {
            'drink_id': wine[0],
            'drink_name': wine[1],
            'description': wine[2],
            'price': wine[3],
            'drink_type': wine[4],
            'ingredients': wine[5]
        }
        wine_list.append(wine_dict)

    return jsonify(wine_list)

### ROUTE ::: BUDGET_DRINKS ###
@app.route('/budget_drinks', methods=['GET'])
def get_budget_drinks():
    # Query the "drinks" table for drinks with a price of 10.99 or lower
    cur.execute("SELECT * FROM drinks WHERE price::numeric <= 10.99")
    budget_drinks = cur.fetchall()

    # Convert the query results to a list of dictionaries
    drink_list = []
    for drink in budget_drinks:
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


# DO NOT TOUCH
if __name__ == '__main__':
    app.run(debug=True)