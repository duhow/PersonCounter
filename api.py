from flask import Flask, request, jsonify, abort

from app import app, redis_db

def get_locations(with_count=False):
    locations = redis_db.lrange("locations", 0, -1)
    if not with_count:
        # as list
        return locations

    data = dict()
    for location in locations:
        path = f"locations/{location}"
        value = redis_db.hget(path, "total")
        data[location] = int(value)

    return data

@app.route("/api/locations", methods=["GET", "POST"])
def api_locations():
    """ Redis: List """
    if request.method == "POST":
        data = request.get_json(force=True)

        if data is None:
            abort(400)
        if 'name' not in data.keys():
            abort(400)

        location = data.get("name")
        locations = get_locations()

        if location in locations:
            abort(409, "Location already repeated")

        query = redis_db.rpush("locations", location)

        api_locations_count(location, "reset")

        return jsonify(
            result=bool(query)
        )

    elif request.method == "GET":
        data = get_locations()
        #print(data)

        return jsonify(
            data=data
        )

@app.route("/api/locations/<location>", methods=["GET"])
def api_location_get(location):
    locations = get_locations()
    if location not in locations:
        abort(404)

    return jsonify(data=get_location_count(location))

@app.route("/api/locations/clear", methods=["POST"])
def api_locations_clear():
    query = redis_db.delete("locations")
    return jsonify(
        result=bool(query)
    )

@app.route("/api/locations/<location>/config", methods=["POST"])
def api_locations_config(location):
    locations = get_locations()
    if location not in locations:
        abort(404)

    data = request.get_json(force=True)
    if not data:
        abort(400)

    path = f"locations/{location}"

    if 'max' in data.keys():
        value = max(int(data["max"]), 0)
        redis_db.hset(path, "max", value)
    else:
        abort(400)

    return jsonify(result=True)

@app.route("/api/locations/<location>/<operation>", methods=["POST"])
def api_locations_count(location, operation):
    locations = get_locations()
    if location not in locations:
        abort(404)

    if operation not in ["in", "add", "out", "sub", "reset"]:
        abort(400)

    path = f"locations/{location}"
    columns = ["total", "in", "out", "max"]

    if operation == 'reset':
        for column in columns:
            redis_db.hset(path, column, 0)
    elif operation in ['in', 'add']:
        redis_db.hincrby(path, "in", 1)
        redis_db.hincrby(path, "total", 1)
    elif operation in ['out', 'sub']:
        redis_db.hincrby(path, "out", 1)
        redis_db.hincrby(path, "total", -1)

    value = get_location_count(location)
    return jsonify(data=value)

def get_location_count(location) -> dict:
    path = f"locations/{location}"

    value = redis_db.hgetall(path)
    for key, val in value.items():
        if isinstance(val, str) and val.isnumeric():
            value[key] = int(val)
    #print(value)
    return value
