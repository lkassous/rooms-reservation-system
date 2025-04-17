from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/reservations', methods=['GET'])
def get_reservations():
    return jsonify([
        {"id": 1, "salle": "Salle A", "utilisateur": "Ali", "date": "2025-04-20"},
        {"id": 2, "salle": "Salle B", "utilisateur": "Sara", "date": "2025-04-21"}
    ])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
