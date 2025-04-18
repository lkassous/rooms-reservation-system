from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/salles', methods=['GET'])
def get_salles():
    return jsonify([
        {"id": 1, "nom": "Salle A"},
        {"id": 2, "nom": "Salle B"}
    ])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

