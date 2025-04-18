from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/reservations', methods=['GET'])
def get_reservations():
    try:
        users = requests.get("http://user-service:5000/users").json()
    except Exception as e:
        users = []
    
    try:
        salles = requests.get("http://salle-service:5000/salles").json()
    except Exception as e:
        salles = []

    return jsonify({
        "reservations": [
            {"id": 1, "salle": salles[0] if salles else {}, "utilisateur": users[0] if users else {}, "date": "2025-04-20"},
            {"id": 2, "salle": salles[1] if len(salles) > 1 else {}, "utilisateur": users[1] if len(users) > 1 else {}, "date": "2025-04-21"}
        ]
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

