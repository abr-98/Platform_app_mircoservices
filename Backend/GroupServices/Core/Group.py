import datetime as dt
from flask_sqlalchemy import SQLAlchemy
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
db: SQLAlchemy = app_creater.get_db()

class Group(db.Model):
    __tablename__="Group"
    
    GroupId = db.Column(db.Text, primary_key=True, unique = True)
    GroupName = db.Column(db.Text, nullable = False)
    Interests = db.Column(db.Text)
    CreationDate = db.Column(db.DateTime)
    Admin = db.Column(db.Text)    
    
    def __init__(self, groupId, name, userId):
        self.GroupId: str = groupId
        self.Admin : str = userId
        self.GroupName : str = name
        self.CreationDate : dt.datetime = dt.datetime.now()
        self.Interests : str = None
        
    @staticmethod
    def from_json(json_dict):
        return Group(json_dict['GroupId'], 
                        json_dict['GroupName'],
                        json_dict['UserId'])
        
    
    def updateInterests(self, interests):
        self.Interests = interests
    
    
        