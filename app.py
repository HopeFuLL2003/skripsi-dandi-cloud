from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

access_logs = []

doors = {
    "door1": {"username": "admin1", "password": "1234", "unlock": False},
    "door2": {"username": "admin2", "password": "5678", "unlock": False},
    "door3": {"username": "admin3", "password": "9999", "unlock": False},
}

@app.route("/")
def home():
    return "Cloud Server Running"

@app.route("/test_unlock/<door_id>")
def test_unlock(door_id):
    if door_id in doors:
        doors[door_id]["unlock"] = True
        return "Unlock triggered"
    return "Door not found"

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    door_id = data.get("door_id")
    username = data.get("username")
    password = data.get("password")

    if door_id in doors:
        if doors[door_id]["username"] == username and doors[door_id]["password"] == password:
            doors[door_id]["unlock"] = True
            return jsonify({"status": "success"})
    return jsonify({"status": "failed"})

@app.route("/remote_status/<door_id>")
def remote_status(door_id):
    if door_id in doors:
        if doors[door_id]["unlock"]:
            doors[door_id]["unlock"] = False
            return jsonify({"unlock": True})
        return jsonify({"unlock": False})
    return jsonify({"unlock": False})

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)

@app.route("/log_access", methods=["POST"])
def log_access():

    data = request.json

    log = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "door": data.get("door_id"),
        "name": data.get("name"),
        "card": data.get("card_uid"),
        "method": data.get("method"),
        "status": data.get("status")
    }

    access_logs.append(log)

    print("NEW LOG:", log)

    return jsonify({"status": "ok"})

@app.route("/logs")
def get_logs():
    return jsonify(access_logs)
