import jwt
import datetime
import os
from flask import (
    Flask,
    request,
    jsonify,
)
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# MySQL configurations
server.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
server.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
server.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
server.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
server.config['MYSQL_PORT'] = os.getenv('MYSQL_PORT')

