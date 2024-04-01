from flask_sqlalchemy import SQLAlchemy
from InteractiveServices.Core.InteractionException import InteractionException
from InteractiveServices.Core.Likes import Likes
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
db: SQLAlchemy = app_creater.get_db()

class LikeDataRepository:
    
    def save(self, like: Likes):
        try:
            db.session.add(like)
            db.session.commit()
        except Exception as e:
            raise InteractionException.WhenInterationOperationFailed(e)
        
    def fetchAll(self, postId: str):
        try:
            likes = Likes.query.filter_by(PostId = postId).all()
            if likes == None:
                return None
            return likes
        except Exception as e:
            raise InteractionException.WhenInterationOperationFailed(e)