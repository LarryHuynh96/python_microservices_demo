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
        return "Missing username or password", 401

    cur = mysql.connection.cursor()
    res = cur.execute(f"SELECT * FROM users WHERE username = '{auth.username}'")

    if res > 0:
        user = cur.fetchone()
        if user[1] != auth.password and user[0] != auth.username:
            return "Invalid credentials", 401
        else:
            return create_jwt(auth.username, os.getenv("SECRET_KEY"), True)
    else:
        return "User not found", 404


def create_jwt(username, secret_key, is_admin):
    payload = {
        "username": username,
        "admin": is_admin,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")

@server.route("/validate", methods=["POST"])
def validate():
    encoded_token = request.headers.get("Authorization")
    if not encoded_token:
        return jsonify({"message": "Missing token"}), 401

    encoded_token = encoded_token.split(" ")[1]
    try:
        decoded_token = jwt.decode(encoded_token, os.getenv("SECRET_KEY"), algorithms=[
            "HS256"])
    except:
        return "Not authorize", 401
    return decoded_token, 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000)
