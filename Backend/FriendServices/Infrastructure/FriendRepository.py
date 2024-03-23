from flask_sqlalchemy import SQLAlchemy
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton
from FriendServices.Core.FriendException import FriendException
from FriendServices.Core.Friend import Friend

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
db: SQLAlchemy = app_creater.get_db()


class FriendRepository:
    
    def addFriend(self, userId: str, FriendId: str):
        try:
            data = Friend(userId,FriendId)
            db.session.add(data)
            db.session.commit()
        except Exception as e:
            raise FriendException.WhenFriendRequestCreationFails(e)
        
    def confirmFriend(self, userId: str, friendId):
        try:
            data :Friend = Friend.query.filter_by(HashKey = self.get_hashkey(friendId,userId)).first()
            data.confirmConnection()
            data_reverse = Friend(userId,friendId)
            data_reverse.confirmConnection()
            db.session.add(data_reverse)
            db.session.commit()
        except Exception as e:
            raise FriendException.WhenRequestStateChangeFails(e)
        
    def blockFriend(self, userId: str, friendId):
        try:
            data :Friend = Friend.query.filter_by(HashKey = self.get_hashkey(friendId,userId)).first()
            if data == None:
                data = Friend(friendId,userId)
                data.blockConnection()
                db.session.add(data)
            else:
                data.blockConnection()
                data_reverse :Friend = Friend.query.filter_by(HashKey = self.get_hashkey(userId,friendId)).first()
                db.session.delete(data_reverse)
            db.session.commit()
        except Exception as e:
            raise FriendException.WhenRequestStateChangeFails(e)
        
    def fetch(self, userId: str, friendId) -> Friend:
        try:
            data :Friend = Friend.query.filter_by(HashKey = self.get_hashkey(userId,friendId)).first()
            return data
        except Exception as e:
            raise FriendException.WhenFriendDataFetchFails(e)
        
    def removeFriend(self, userId: str, friendId) -> Friend:
        try:
            data :Friend = Friend.query.filter_by(HashKey = self.get_hashkey(userId,friendId)).first()
            data_reverse :Friend = Friend.query.filter_by(HashKey = self.get_hashkey(friendId,userId)).first()
            db.session.delete(data_reverse)
            db.session.delete(data)
            db.session.commit()
            return data
        except Exception as e:
            raise FriendException.WhenFriendRemovalFails(e)
        
        
    def unblockFriend(self, userId: str, friendId) -> Friend:
        try:
            data :Friend = Friend.query.filter_by(HashKey = self.get_hashkey(friendId,userId)).first()
            db.session.delete(data)
            db.session.commit()
            return data
        except Exception as e:
            raise FriendException.WhenFriendRemovalFails(e)
        
    def get_hashkey(self, userId, friendId):
        return f"{userId}_{friendId}"