from UserServices.Core.UserExceptions import UserException
from UserServices.Core.User import User
from flask_sqlalchemy import SQLAlchemy
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
db: SQLAlchemy = app_creater.get_db()

class UserRepository:
        
    def save(self, user: User):
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            raise UserException.WhenUserCreationFails(e)
        
    def update(self, field, value, userId):
        try:
            data :User = User.query.filter_by(UserId = userId).first()
            if data == None:
                raise UserException.WhenUserDoesnotExist()
            data.updateValue(field, value)
            db.session.commit()
        except Exception as e:
            if e.__class__.__base__ != UserException:
                raise UserException.WhenUserUpdationFails(e)
            else:
                raise e
        
    def Verify(self, userId):
        try:
            data :User = User.query.filter_by(UserId = userId).first()
            data.verifUser()
            db.session.commit()
        except Exception as e:
            raise UserException.WhenUserVerificationFails(e)
        
    def fetch(self, userId) -> User:
        try:
            data :User = User.query.filter_by(UserId = userId).first()
            if data == None:
                return None
            return data
        except Exception as e:
            raise UserException.WhenUserFetchFails(e)
            
    def delete(self, userId):
        try:
            data :User = User.query.filter_by(UserId = userId).first()
            if data == None:
                raise UserException.WhenUserDoesnotExist()
            db.session.delete(data)
            db.session.commit()
        except Exception as e:
            if e.__class__.__base__ != UserException:
                raise UserException.WhenUserFetchFails(e)
            else:
                raise e
    
    def fetchByField(self, field , value) -> User:
        try:
            data :User = User.query.filter(getattr(User, field)== value).first()
            if data == None:
                return None
            return data
        except Exception as e:
            raise UserException.WhenUserFetchFails(e)
        
        
        
        
        
        
        
        
        
        
