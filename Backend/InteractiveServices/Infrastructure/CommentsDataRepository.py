from flask_sqlalchemy import SQLAlchemy
from InteractiveServices.Core.InteractionException import InteractionException
from InteractiveServices.Core.Comments import Comments
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
db: SQLAlchemy = app_creater.get_db()

class CommentDataRepository:
    
    def save(self, comment: Comments):
        try:
            db.session.add(comment)
            db.session.commit()
        except Exception as e:
            raise InteractionException.WhenInterationOperationFailed(e)
        
    def fetchAll(self, postId: str):
        try:
            likes = Comments.query.filter_by(PostId = postId).all()
            if likes == None:
                return None
            return likes
        except Exception as e:
            raise InteractionException.WhenInterationOperationFailed(e)