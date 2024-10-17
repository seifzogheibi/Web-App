from flask_sqlalchemy import SQLAlchemy

#class Property(db.Model):
   # id = db.Column(db.Integer, primary_key=True)
   # address = db.Column(db.String(500), index=True, unique=True)
   # start_date = db.Column(db.DateTime)
  #  duration = db.Column(db.Integer)
    #rent = db.Column(db.Float)
db = SQLAlchemy()

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    module_code = db.Column(db.String(10), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)