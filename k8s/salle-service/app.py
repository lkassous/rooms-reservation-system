from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Salle
from kafka import KafkaProducer
import json, time, os
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")

db.init_app(app)

def wait_for_postgres():
    while True:
        try:
            conn = psycopg2.connect(os.getenv("DATABASE_URL"))
            conn.close()
            break
        except Exception as e:
            print("🔁 Attente de PostgreSQL...")
            time.sleep(2)

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
            time.sleep(2)

wait_for_postgres()
with app.app_context():
    db.create_all()

producer = wait_for_kafka()

# ✅ Route racine pour vérifier le bon fonctionnement
@app.route('/')
def index():
    return "✅ User-service est en ligne !"

# ✅ Route d'entrée utilisée par Ingress
@app.route('/user')
def user_root():
    return "✅ Route /user OK depuis Ingress"

@app.route('/salles', methods=['GET'])
def get_salles():
    salles = Salle.query.all()
    return jsonify([{"id": s.id, "nom": s.nom} for s in salles])

@app.route('/salles', methods=['POST'])
def add_salle():
    data = request.get_json()
    salle = Salle(id=data['id'], nom=data['nom'])
    db.session.add(salle)
    db.session.commit()
    producer.send('salles', data)
    return jsonify({"message": "✅ Salle créée et événement envoyé à Kafka"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

