from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    utilisateur = db.Column(db.String(100), nullable=False)
    salle = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)

