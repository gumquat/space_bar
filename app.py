from flask import Flask, jsonify, redirect, url_for, request, session, flash, render_template
from flask_caching import Cache
import psycopg2
import logging
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
import logging

LOG_FORMAT = "%(levelname)s %(asctime)s - %(name)s - %(message)s"
logging.basicConfig(filename='./logs/app.log',
                    level=logging.DEBUG,
                    format=LOG_FORMAT,
                    filemode='a')
logger = logging.getLogger('appLogger')

# Get the environment variables from the .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

bcrypt = Bcrypt(app)

logger.info("Starting Flask application")
logger.info("Loading configuration...")

# Configure the cache
app.config.from_mapping(
    CACHE_TYPE="simple",
    CACHE_DEFAULT_TIMEOUT=300  # Cache duration in seconds
)
cache = Cache(app)

# Database configuration
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')

# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    logger.info("Successfully connected to the database.")
except psycopg2.OperationalError as e:
    logger.critical(f"Failed to connect to the database: {e}")

# Create a cursor object
cur = conn.cursor()

@app.before_request
def before_request_log():
    logger.debug(f"Handling request: {request.path}")


@app.after_request
def after_request_log(response):
    logger.debug(f"Handled request: {request.path} - Response status: {response.status_code}")
    return response


@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {e}", exc_info=True)
    return "An internal error occured.", 500

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the form data
        username = request.form['username']
        password = request.form['password']

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insert the user data into the "users" table
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()

        flash('You have successfully registered. Please log in.', 'success')
        return jsonify({'message': 'You have successfully registered. Please log in.'})
        # return redirect(url_for('login'))
    
    return jsonify({'message': 'Please register to access this page'})
    # return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the form data
        username = request.form['username']
        password = request.form['password']

        # Query the "users" table for the user
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        if user and bcrypt.check_password_hash(user[2], password):
            # Check if the password is correct
            session['user_id'] = user[0]
            session['username'] = user[1]

            flash('You have successfully signed in as ' + username, 'success')
            return jsonify({'message': 'You have successfully signed in as ' + username})
            # return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return jsonify({'message': 'Login Unsuccessful. Please check username and password'})
            # return redirect(url_for('login'))
    
    return jsonify({'message': 'Please log in to access this page'})
    # return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'success')
    return jsonify({'message': 'You have been logged out'})
    # return redirect(url_for('login'))

# Decorator to check if the user is logged in    
def login_required(func):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('You ust be logged in to view this page', 'danger')
            return jsonify({'message': 'You ust be logged in to view this page'})
            # return redirect(url_for('login'))
        return func(*args, **kwargs)
    return wrapper

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'What is money called in space? Star bucks!'})



# ### ROUTE ::: ALL DRINKS ###
@app.route('/drinks', methods=['GET'])
@cache.cached(timeout=300)
def get_all_drinks():
    """Route that GETS all drinks from entire database
    """
    logger.info("Fetching all drinks")
    try:
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
    except Exception as e:
        logger.error(f"Failed to fetch drinks: {e}")
        return "An error occured!", 500


# ### ROUTE ::: COCKTAILS ###
@app.route('/cocktails', methods=['GET'])
@cache.cached(timeout=300)
def get_cocktails():
    """Route that GETS all drinks of type 'cocktail'
    """
    logger.info("Fetching Cocktails")
    try:
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
    except Exception as e:
        logger.error(f"Failed to fetch cocktails: {e}")
        return "An error occured!", 500


# ### ROUTE ::: COCKTAILS ###
@app.route('/beers', methods=['GET'])
@cache.cached(timeout=300)
def get_beers():
    """Route that GETS all drinks of type 'beer'
    """
    logger.info("Fetching Beers")
    try:
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
                # 'ingredients': beer[5]
            }
            beer_list.append(beer_dict)

        return jsonify(beer_list)
    except Exception as e:
        logger.error(f"Failed to fetch beers: {e}")
        return "An error occured!", 500


# ### ROUTE ::: WINE ###
@app.route('/wines', methods=['GET'])
@cache.cached(timeout=300)
def get_wines():
    """Route that GETS all drinks of type 'wine'
    """
    logger.info("Fetching Wines")
    try:
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
    except Exception as e:
        logger.error(f"Failed to fetch wines: {e}")
        return "An error occured!", 500


# ### ROUTE ::: BUDGET_DRINKS ###
@app.route('/budget_drinks', methods=['GET'])
@cache.cached(timeout=300)
def get_budget_drinks():
    """Route that GETS drinks with a price value of or less than '10.99'
    """
    logger.info("Fetching Budget Drinks")
    try:
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
    except Exception as e:
        logger.error(f"Failed to fetch budget drinks: {e}")
        return "An error occured!", 500


# DO NOT TOUCH
if __name__ == '__main__':
    app.run(debug=True)
