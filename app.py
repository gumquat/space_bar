from flask import Flask, jsonify, redirect, url_for, request, session, flash, render_template
from flask_caching import Cache
import psycopg2
import logging
from flask_bcrypt import Bcrypt
from functools import wraps
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
conn = None
try:
    conn = psycopg2.connect(
        dbname=os.environ.get("POSTGRES_DB"),
        user=os.environ.get("POSTGRES_USER"),
        password=os.environ.get("POSTGRES_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT")
    )
    logger.info("Successfully connected to the database.")
except psycopg2.OperationalError as e:
    logger.critical(f"Failed to connect to the database: {e}")
    raise e

# Create a cursor object
if conn:
    cur = conn.cursor()
else:
    logger.critical("Database connection was not established. Exiting.")


@app.before_request
def before_request_log():
    logger.debug(f"Handling request: {request.path}")


@app.after_request
def after_request_log(response):
    logger.debug(
        f"Handled request: {request.path} - "
        f"Response status: {response.status_code}"
    )
    return response


@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {e}", exc_info=True)
    return "An internal error occured.", 500


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the form data
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insert the user data into the "users" table
        try:
            cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, hashed_password, email))
            conn.commit()
            logger.info(f'User registered: {username}')
            flash('You have successfully registered. Please log in.', 'success')
            return jsonify({'message': 'You have successfully registered. Please log in.'}), 200
            # return redirect(url_for('login'))
        except Exception as e:
            logger.error(f'Failed to register user {username}: {e}')
            return jsonify({'message': 'Registration failed'}), 500

    return jsonify({'message': 'Please register to access this page'})
    # return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the form data
        username = request.form['username']
        password = request.form['password']

        # Query the "users" table for the user
        try:
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cur.fetchone()

            if user and bcrypt.check_password_hash(user[2], password):
                # Check if the password is correct
                session['user_id'] = user[0]
                session['username'] = user[1]
                logger.info(f'User logged in: {username}')
                flash('You have successfully signed in as ' + username, 'success')
                return jsonify({'message': 'You have successfully signed in as ' + username}), 200
                # return redirect(url_for('home'))
            else:
                logger.warning(f'Login failed for: {username}')
                flash('Login Unsuccessful. Please check username and password', 'danger')
                return jsonify({'message': 'Login Unsuccessful. Please check username and password'}), 401
                # return redirect(url_for('login'))
        except Exception as e:
            logger.error(f'Error during login for {username}: {e}')
            return jsonify({'message': 'Error processing login'}), 500

    return jsonify({'message': 'Please log in to access this page'})
    # return render_template('login.html')


@app.route('/logout')
def logout():
    logger.info(f'User logged out: {session.get("username")}')
    session.pop('user_id', None)
    flash('You have been logged out', 'success')
    return jsonify({'message': 'You have been logged out'}), 200
    # return redirect(url_for('login'))


# Decorator to check if the user is logged in
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            logger.warning(f'Unauthorized access attempt to {func.__name__}')
            flash('You must be logged in to view this page', 'danger')
            return jsonify({'message': 'You must be logged in to view this page'}), 403
            # return redirect(url_for('login'))
        logger.info(f'Access granted for {func.__name__} to user {session.get("username")}'), 200
        return func(*args, **kwargs)
    return wrapper


@app.route('/dashboard')
@login_required
def dashboad():
    logger.info(f'Dashboard accessed by {session.get("username")}')
    return jsonify({'message': f'Welcome to your dashboard, {session.get("username")}!'})


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

        return jsonify(drink_list), 200
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
            cocktail_list.append(cocktail_dict), 200

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
            beer_list.append(beer_dict), 200

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

        return jsonify(wine_list), 200
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
            drink_list.append(drink_dict), 200

        return jsonify(drink_list)
    except Exception as e:
        logger.error(f"Failed to fetch budget drinks: {e}")
        return "An error occured!", 500

# ### ROUTE ::: LIQUORS ###
@app.route('/liquors', methods=['GET'])
@cache.cached(timeout=300)
def get_liquors():
    """Route that GETS all drinks of type 'liquor'
    """
    logger.info("Fetching Liquors")
    try:
        # Query the "drinks" table for drinks with a drink_type of 'liquor'
        cur.execute("SELECT * FROM drinks WHERE drink_type = 'Liquor'")
        liquors = cur.fetchall()

        # Convert the query results to a list of dictionaries
        liquor_list = []
        for liquor in liquors:
            liquor_dict = {
                'drink_id': liquor[0],
                'drink_name': liquor[1],
                'description': liquor[2],
                'price': liquor[3],
                'drink_type': liquor[4],
                'ingredients': liquor[5]
            }
            liquor_list.append(liquor_dict)

        return jsonify(liquor_list), 200
    except Exception as e:
        logger.error(f"Failed to fetch liquors: {e}")
        return "An error occurred!", 500

# DO NOT TOUCH
if __name__ == '__main__':
    app.run(debug=True)
