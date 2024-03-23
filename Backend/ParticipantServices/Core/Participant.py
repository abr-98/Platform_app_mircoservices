import datetime as dt
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
db: SQLAlchemy = app_creater.get_db()

POSSIBLE_STATUSES = Enum("POSSIBLE_STATUSES", ["Member", "Requested", "Add_request_pending", "Blocked"])

class Participant(db.Model):
    __tablename__="Participant"
    
    Hash = db.Column(db.Text, primary_key=True, unique = True)
    UserId = db.Column(db.Text, nullable=False)
    GroupId = db.Column(db.Text, nullable=False)
    DateOfJoining = db.Column(db.DateTime)
    Status = db.Column(db.Text)
    
    
    def __init__(self, userId, groupId, status):
        self.Hash : str = f"{userId}_{groupId}"
        self.UserId : str = userId
        self.GroupId : str = groupId
        self.DateOfJoining: dt.datetime = dt.datetime.now()
        self.Status: str = status
    
    def Confirm_Participant(self):
        self.Status = POSSIBLE_STATUSES.Member.value
        
    def Block_Participant(self):
        self.Status = POSSIBLE_STATUSES.Blocked.value

        
     
