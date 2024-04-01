from flask_sqlalchemy import SQLAlchemy
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton
from PostServices.Core.Post import Post
from PostServices.Core.PostException import PostException
from app import logger

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
db: SQLAlchemy = app_creater.get_db()

class PostRepository:
    
    def save(self, post: Post):
        try:
            db.session.add(post)
            db.session.commit()
            logger.info("post saved")
        except Exception as e:
            raise PostException.WhenPostCreationFails(e)
        
    def fetchAllforUser(self, userId) -> Post:
        try:
            data :Post = Post.query.filter_by(UserId = userId).all()
            logger.info("post fetched")
            if data == None:
                return None
            return data
        except Exception as e:
            raise PostException.WhenPostFetchFails(e)
        
    def fetch(self, postId) -> Post:
        try:
            data :Post = Post.query.filter_by(PostId = postId).first()
            logger.info("post fetched")
            if data == None:
                return None
            return data
        except Exception as e:
            raise PostException.WhenPostFetchFails(e)
        
    def delete(self, postId) -> Post:
        try:
            data :Post = Post.query.filter_by(PostId = postId).first()
            db.session.delete(data)
            db.session.commit()
            logger.info("post deleted")
        except Exception as e:
            raise PostException.WhenPostFetchFails(e)
        