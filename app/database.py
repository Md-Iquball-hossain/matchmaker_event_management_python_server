# Author: Shidul Islam
# Date: 10-11-2023
# */

import psycopg2
from flask import Flask
import logging
from psycopg2 import pool
from config import DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT

app = Flask(__name__)

# Configure the logger
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Define the connection parameters
params = {
    'database': DB_NAME,
    'user': DB_USER,
    'password': DB_PASS,
    'host': DB_HOST,
    'port': DB_PORT,
}

try:
    # Attempt to establish a connection
    # conn = psycopg2.connect(**params) ->   /// TODO -> It's the connection without pool
    conn = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=20,
        **params
    )
    print("Connected to PostgreSQL with user")
except psycopg2.Error as e:
    print("Error: Unable to connect to PostgreSQL")
    print(e)
