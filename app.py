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

# ROUTE ::: COCKTAILS
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