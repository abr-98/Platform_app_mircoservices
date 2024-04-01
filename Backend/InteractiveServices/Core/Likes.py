from flask_sqlalchemy import SQLAlchemy
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
db: SQLAlchemy = app_creater.get_db()


class Likes(db.Model):    
    __tablename__="Likes"
    
    HashKey = db.Column(db.Text, primary_key=True, unique = True)
    UserId = db.Column(db.Text, nullable = False)
    PostId = db.Column(db.Text, nullable = False)
    
    def __init__(self, userId, postId):
        self.HashKey = f"{userId}_{postId}"
        self.UserId = userId
        self.PostId = postId