from flask_sqlalchemy import SQLAlchemy
from Status_Maintainance_Services.Core.Status import Status
from Status_Maintainance_Services.Core.OnlineStatusException import OnlineStatusException
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton
import datetime as dt

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
db: SQLAlchemy = app_creater.get_db()

class StatusRepository:
        
    def save(self, status: Status):
        try:
            data: Status = Status.query.filter_by(Hash = self.get_hash(status.UserId, status.IP)).first()
            if data != None:
                data.LoginDate = dt.datetime.now()
            else:
                db.session.add(status)
            db.session.commit()
        except Exception as e:
            raise OnlineStatusException.WhenStatusChangeFails(e)
        
    def fetch(self, userId: str, IP: str):
        try:
            data = Status.query.filter_by(Hash = self.get_hash(userId, IP)).first()
            if data == None:
                return None
            return data
        except Exception as e:
             raise OnlineStatusException.WhenStatusFetchFails(e)
         
    def delete(self, userId: str, IP: str):
        try:
            data = Status.query.filter_by(Hash = self.get_hash(userId, IP)).first()
            if data == None:
                raise OnlineStatusException.WhenUserNotLoggedIn(userId)
            db.session.delete(data)
            db.session.commit()
        except Exception as e:
            if e.__class__.__base__ != OnlineStatusException:
                raise OnlineStatusException.WhenStatusChangeFails(e)
            else:
                raise e
        
    def get_hash(self,userId: str, Ip: str):
        return f"{userId}_{Ip}"