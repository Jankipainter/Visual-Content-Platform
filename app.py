from flask import Flask,session
from flask_session import Session
import mysql.connector
import os

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
# app.secret_key=b'secret@j@1712'


# Replace these values with your actual database information
host = "localhost"
user = "root"
password = "Root@123"
database = "pintrestdb"
port=3307
auth_plugin="mysql_native_password"

# Create a database connection
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port,
    auth_plugin=auth_plugin
)

# Create a cursor
cursor = connection.cursor()
# db=cursor(app)

