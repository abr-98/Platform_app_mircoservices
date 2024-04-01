from flask_sqlalchemy import SQLAlchemy
import datetime as dt
from Utility_Module.IdGenerator import IdGenerator

from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
db: SQLAlchemy = app_creater.get_db()
idgenerator = IdGenerator()

class Post(db.Model):
    __tablename__ = "Post"
    
    PostId = db.Column(db.Text, primary_key= True, nullable = False)
    UserId = db.Column(db.Text, nullable = False)
    Path = db.Column(db.Text)
    CreatedDate = db.Column(db.DateTime)
    Tags = db.Column(db.Text)
    Description = db.Column(db.Text)
    
    def __init__(self, UserId, Tags, Description):
            self.PostId = idgenerator.GenerateUniqueId()
            self.UserId = UserId
            self.Tags = Tags
            self.Description = Description
            self.Path = f"{UserId}/{self.PostId}"
            self.CreateDate = dt.datetime.now()
        
    @staticmethod
    def from_json(json_dict):
        return Post(json_dict['UserId'], 
                        json_dict['Tags'],
                        json_dict['Description'])
        

