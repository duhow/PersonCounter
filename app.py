from flask import Flask
import redis

app = Flask(__name__)

redis_db = redis.Redis(host='localhost', port=6379, db=0)

import api

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
