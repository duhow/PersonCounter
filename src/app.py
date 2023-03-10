from flask import Flask, render_template, abort
import redis
import os

app = Flask(__name__)

redis_db = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=os.getenv('REDIS_PORT', 6379),
    db=os.getenv('REDIS_DB', 0),
    charset="utf-8",
    decode_responses=True # set as str, not bytes
)

import api

@app.route("/")
def web_locations():
    locations = api.get_locations(with_count=True)
    return render_template('locations.html', locations=locations)

@app.route("/<location>")
def web_location(location):
    locations = api.get_locations()
    if not location in locations:
        abort(404)

    return render_template('counter.html', location=location)
