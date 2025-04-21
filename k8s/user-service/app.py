from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, User
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

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{"id": u.id, "nom": u.nom} for u in users])

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    user = User(id=data['id'], nom=data['nom'])
    db.session.add(user)
    db.session.commit()
    producer.send('users', data)
    return jsonify({"message": "✅ Utilisateur créé et événement envoyé à Kafka"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

