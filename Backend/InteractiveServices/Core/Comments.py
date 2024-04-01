from flask_sqlalchemy import SQLAlchemy
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton
import datetime as dt

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
db: SQLAlchemy = app_creater.get_db()


class Comments:
    __tablename__="Comments"
    
    HashKey = db.Column(db.Text, primary_key=True, unique = True)
    UserId = db.Column(db.Text, nullable = False)
    PostId = db.Column(db.Text, nullable = False)
    TimeStamp = db.Column(db.DateTime)
    Comment = db.Column(db.Text, nullable = False)
    
    def __init__(self, userId, postId, Comment):
        self.HashKey = f"{userId}_{postId}"
        self.UserId = userId
        self.PostId = postId
        self.Comment = Comment
        self.TimeStamp = dt.datetime.now()
        
    @staticmethod
    def from_json(json_dict):
        return Comments(json_dict['UserId'], 
                        json_dict['PostId'],
                        json_dict['Comment'])
        
    