from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from kafka import KafkaProducer
import json
import time
import os

app = Flask(__name__)

# Config base de données
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://admin:admin@localhost:5432/reservationsdb")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle Reservation
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    salle_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(20), nullable=False)

# Fonction pour attendre Kafka avant d'établir une connexion
def wait_for_kafka():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            print("✅ Kafka connecté avec succès.")
            return producer
        except Exception:
            print("🔁 Attente de Kafka...")
            time.sleep(5)

producer = wait_for_kafka()

# Initialiser la base de données
with app.app_context():
    db.create_all()

# Route GET pour voir les réservations
@app.route('/reservations', methods=['GET'])
def get_reservations():
    reservations = Reservation.query.all()
    result = [
        {"id": r.id, "user_id": r.user_id, "salle_id": r.salle_id, "date": r.date}
        for r in reservations
    ]
    return jsonify(result)

# Route POST pour ajouter une réservation
@app.route('/reservations', methods=['POST'])
def add_reservation():
    try:
        data = request.get_json()
        reservation = Reservation(
            user_id=data['user_id'],
            salle_id=data['salle_id'],
            date=data['date']
        )
        db.session.add(reservation)
        db.session.commit()

        # Envoyer à Kafka
        producer.send('reservations', {
            "user_id": reservation.user_id,
            "salle_id": reservation.salle_id,
            "date": reservation.date
        })

        return jsonify({"message": "✅ Réservation créée avec succès"}), 201
    except Exception as e:
        print("❌ Erreur lors de la création de la réservation:", e)
        return jsonify({"error": "Erreur interne"}), 500

# Route d'accueil
@app.route('/', methods=['GET'])
def home():
    return "✅ Reservation Service est en ligne !"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

