import os
import pytest
import psycopg2
from app import app
from dotenv import load_dotenv

#load the environment variables from .env file
load_dotenv()

@pytest.fixture
def client():
    app.config['TESTING'] = True

    test_conn = psycopg2.connect(
        dbname=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    test_conn.autocommit = False
    test_cur = test_conn.cursor()

    global conn, cur
    conn, cur = test_conn, test_cur
    
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client
            cleanup_test_user()

    test_conn.rollback()
    test_cur.close()
    test_conn.close()

    conn, cur = None, None

def cleanup_test_user():
    host = os.getenv('DB_HOST')
    database = os.getenv('POSTGRES_DB')
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')

    conn = psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password
    )

    cur = conn.cursor()

    cur.execute("DELETE FROM users WHERE username = 'testuser'")
    conn.commit()

    cur.close()
    conn.close()

def test_register_post(client):
    # test the register function with a valid user
    response = client.post('/register', data ={
        'email': 'test@email.com',
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert b'You have successfully registered. Please log in.' in response.data

def test_register_post_existing_user(client):
    # test the register function with an existing user
    response = client.post('/register', data ={
        'email': 'test@email.com',
        'username': 'testuser',
        'password': 'testpassword'
    })
    
    response = client.post('/register', data ={
        'email': 'test@email.com',
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 500
    assert b'Registration failed' in response.data

def test_register_post_no_email(client):
    # test the register function with no username
    response = client.post('/register', data ={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 400
    assert b'Please provide all required fields' in response.data

def test_register_post_no_user_name(client):
    # test the register function with no username
    response = client.post('/register', data ={
        'email': 'test@email.com',
        'password': 'testpassword'
    })
    assert response.status_code == 400
    assert b'Please provide all required fields' in response.data

def test_register_post_no_password(client):
    # test the register function with no username
    response = client.post('/register', data ={
        'email': 'test@email.com',
        'username': 'testuser'
    })
    assert response.status_code == 400
    assert b'Please provide all required fields' in response.data

def test_register_get_no_data(client):
    # test the register function with no username
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Please register to access this page' in response.data

def test_login_post(client):
    # test the login function with a valid user
    response = client.post('/register', data ={
        'email': 'test@email.com',
        'username': 'testuser',
        'password': 'testpassword'
    })
    
    response = client.post('/login', data ={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert b'You have successfully signed in as testuser' in response.data

def test_login_post_invalid_user(client):
    # test the login function with an invalid user
    response = client.post('/register', data ={
        'email': 'test@email.com',
        'username': 'testuser',
        'password': 'testpassword'
    })

    response = client.post('/login', data ={
        'username': 'invaliduser',
        'password': 'testpassword'
    })
    assert response.status_code == 401
    assert b'Login Unsuccessful. Please check username and password' in response.data

def test_login_post_invalid_password(client):
    # test the login function with an invalid user
    response = client.post('/register', data ={
        'email': 'test@email.com',
        'username': 'testuser',
        'password': 'testpassword'
    })

    response = client.post('/login', data ={
        'username': 'testuser',
        'password': 'invalidpassword'
    })
    assert response.status_code == 401
    assert b'Login Unsuccessful. Please check username and password' in response.data

def test_login_get_no_data(client):
    # test the login function with no user
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Please log in to access this page' in response.data

def test_logout_post(client):
    # test the logout function with a valid user
    response = client.post('/register', data ={
        'email': 'test@email.com',
        'username': 'testuser',
        'password': 'testpassword'
    })
    
    response = client.post('/login', data ={
        'username': 'testuser',
        'password': 'testpassword'
    })
    
    response = client.get('/logout')
    assert response.status_code == 200
    assert b'You have been logged out' in response.data

def test_logout_get_no_data(client):
    # test the logout function with no user
    response = client.get('/logout')
    assert response.status_code == 200
    assert b'You have been logged out' in response.data
