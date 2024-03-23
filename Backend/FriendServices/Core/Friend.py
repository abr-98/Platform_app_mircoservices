import datetime as dt
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
db: SQLAlchemy = app_creater.get_db()

POSSIBLE_STATUSES = Enum("POSSIBLE_STATUSES", ["Pending", "Confirmed", "Blocked"])

class Friend(db.Model):
    __tablename__ = "Friend"
    
    HashKey = db.Column(db.Text, primary_key=True, unique = True)
    UserId = db.Column(db.Text, nullable = False)
    FriendId = db.Column(db.Text, nullable = False)
    Status = db.Column(db.Text)
    ConnectionDate = db.Column(db.DateTime)
    
    def __init__(self, userId, friendId):
        self.HashKey =f"{userId}_{friendId}"
        self.UserId = userId
        self.FriendId = friendId
        self.Status = POSSIBLE_STATUSES.Pending.value
        self.ConnectionDate = dt.datetime.now()
        
    def confirmConnection(self):
        self.Status = POSSIBLE_STATUSES.Confirmed.value
        self.ConnectionDate = dt.datetime.now()
        
    def blockConnection(self):
        self.Status = POSSIBLE_STATUSES.Blocked.value
        