from flask import Flask, request, jsonify, abort

from app import app, redis_db

def get_locations() -> list:
    query = redis_db.lrange("locations", 0, -1)
    data = list()
    if query:
        data = [x.decode() for x in query]
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
        redis_db.set(f"locations/{location}", 0)

        return jsonify(
            result=bool(query)
        )

    elif request.method == "GET":
        data = get_locations()
        print(data)

        return jsonify(
            data=data
        )

@app.route("/api/locations/clear", methods=["POST"])
def api_locations_clear():
    query = redis_db.delete("locations")
    return jsonify(
        result=bool(query)
    )

@app.route("/api/locations/<location>/<operation>", methods=["POST"])
def api_locations_count(location, operation):
    locations = get_locations()
    if location not in locations:
        abort(404)

    if operation not in ["add", "sub", "reset"]:
        abort(400)

    path = f"locations/{location}"

    if operation == 'reset':
        value = redis_db.set(path, 0)
    elif operation == 'add':
        value = redis_db.incr(path)
    elif operation == 'sub':
        value = redis_db.decr(path)

    return jsonify(result=value)
