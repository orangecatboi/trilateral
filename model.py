from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Enquiry(db.Model):
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100))
    company    = db.Column(db.String(100))
    contact    = db.Column(db.String(100))
    type       = db.Column(db.String(100))
    message    = db.Column(db.Text)

class Application(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(100))
    email    = db.Column(db.String(100))
    phone    = db.Column(db.String(50))
    position = db.Column(db.String(100))
    experience = db.Column(db.String(50))
    cover    = db.Column(db.Text)
    link     = db.Column(db.String(200))