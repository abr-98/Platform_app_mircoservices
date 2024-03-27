from GroupServices.Core.GroupException import GroupException
from GroupServices.Core.Group import Group
from flask_sqlalchemy import SQLAlchemy
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
db: SQLAlchemy = app_creater.get_db()

class GroupDataRepository:
    def save(self, group: Group):
        try:
            db.session.add(group)
            db.session.commit()
        except Exception as e:
            raise GroupException.WhenGroupCreationFails(e)
        
    def fetch(self, groupId: str) -> Group:
        try:
            data: Group = Group.query.filter_by(GroupId = groupId).first()
            if data == None:
                return None
            return data
        except Exception as e:
            raise GroupException.WhenGroupFetchFails(e)
        
    def update_interest(self, groupId: str, interest : str):
        try:
            data: Group = Group.query.filter_by(GroupId = groupId).first()
            if(data == None):
                raise GroupException.WhenGroupDoesNotExist(groupId)
            data.updateInterests(interest)
            db.session.commit()
        except Exception as e:
            if e.__class__.__base__ != GroupException:
                raise GroupException.WhenGroupUpdationFailed(e)
            else:
                raise e
            
    def delete(self, groupId: str):
        try:
            data: Group = Group.query.filter_by(GroupId = groupId).first()
            if(data == None):
                raise GroupException.WhenGroupDoesNotExist(groupId)
            db.session.delete(data)
            db.session.commit()
        except Exception as e:
            if e.__class__.__base__ != GroupException:
                raise GroupException.WhenGroupUpdationFailed(e)
            else:
                raise e
        