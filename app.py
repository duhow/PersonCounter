from flask import Flask, render_template
import redis

app = Flask(__name__)

redis_db = redis.Redis(host='localhost', port=6379, db=0)

import api

@app.route("/")
def web_locations():
    locations = api.get_locations()
    return render_template('locations.html', locations=locations)
