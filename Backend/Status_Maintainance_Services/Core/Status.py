import datetime as dt
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
db: SQLAlchemy = app_creater.get_db()

class Status(db.Model):
    __tablename__="Status"
    
    Hash = db.Column(db.Text, primary_key = True, unique = True)
    UserId = db.Column(db.Text, unique = True)
    IP = db.Column(db.Text, nullable=False)
    LoginDate = db.Column(db.DateTime)
    
    def __init__(self, userId, ip):
        self.Hash : str = f"{userId}_{ip}"
        self.IP : str = ip 
        self.UserId : str = userId
        self.LoginDate : dt.datetime = dt.datetime.now()