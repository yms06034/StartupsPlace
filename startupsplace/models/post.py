from startupsplace import db
from sqlalchemy import func

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db)