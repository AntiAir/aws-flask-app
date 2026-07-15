from flask import Flask, jsonify
import socket
from datetime import datetime
import mysql.connector
import boto3
import json

app = Flask(__name__)

def get_db_secret():
    client = boto3.client(
        "secretsmanager",
        region_name="us-east-1"
    )

    response = client.get_secret_value(
        SecretId="prod/rds/mysql"
    )

    return json.loads(response["SecretString"])


@app.route("/health")
def health():
    return jsonify({
        "status":"healthy"
    })


@app.route("/users")
def users():

    secret = get_db_secret()

    conn = mysql.connector.connect(
        host=secret["host"],
        user=secret["username"],
        password=secret["password"],
        database="appdb"
    )

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(result)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080
    )