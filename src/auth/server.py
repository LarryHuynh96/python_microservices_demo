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
server.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.getenv("MYSQL_DB")
server.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
server.config["MYSQL_PORT"] = os.getenv("MYSQL_PORT")


@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Missing username or password"}), 401

    cur = mysql.connection.cursor()
    res = cur.execute(f"SELECT * FROM users WHERE username = '{auth.username}'")

    if res > 0:
        user = cur.fetchone()
        if user[1] != auth.password and user[0] != auth.username:
            return jsonify({"message": "Invalid credentials"}), 401
        else:
            return jsonify(
                {
                    "token": jwt.encode(
                        {
                            "user": auth.username,
                            "exp": datetime.datetime.utcnow()
                            + datetime.timedelta(minutes=30),
                        },
                        os.getenv("JWT_SECRET_KEY"),
                    )
                }
            )
    else:
        return jsonify({"message": "User not found"}), 404
