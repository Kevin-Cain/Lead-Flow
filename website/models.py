from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func 
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    lead = db.relationship('Leads')

class Leads(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    Name = db.Column(db.String(150))
    Email = db.Column(db.String(150))
    Phone = db.Column(db.String(150))
    BuildCity = db.Column(db.String(150))
    BuildState = db.Column(db.String(150))
    ModelofInterest = db.Column(db.String(150))
    Bedrooms = db.Column(db.String(150))
    Bathrooms = db.Column(db.String(150))
    SquareFootage = db.Column(db.String(150))
    ProductSeries = db.Column(db.String(150))
    AccountName = db.Column(db.String(150))
    DBAAccountName = db.Column(db.String(150))
    AccountAddress = db.Column(db.String(150))
    AccountCity = db.Column(db.String(150))
    AccountState = db.Column(db.String(150))
    AccountZip = db.Column(db.String(150))
    LeadSource = db.Column(db.String(150))
    ConstructionCode = db.Column(db.String(150))
    ConstructionType = db.Column(db.String(150))
    Timing = db.Column(db.String(150))
    HomePlacement = db.Column(db.String(150))
    HasFinancing = db.Column(db.String(150))
    Budget = db.Column(db.String(150))
    DownPayment = db.Column(db.String(150))
    CustomerComments = db.Column(db.Text(length=None))
    Notes = db.Column(db.Text(length=None))

    



    


