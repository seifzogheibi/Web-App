from app import db


# Initializing all the data types that will be
# used to create the assessment tracker
class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    module_code = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)
