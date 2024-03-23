from ParticipantServices.Core.ParticipantException import ParticipantException
from flask_sqlalchemy import SQLAlchemy
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton
from ParticipantServices.Core.Participant import Participant

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
db: SQLAlchemy = app_creater.get_db()

class ParticipantsDataRepository:
    def save(self, participant: Participant):
        try:
            db.session.add(participant)
            db.session.commit()
        except Exception as e:
            raise ParticipantException.WhenParticipantCreationFailed(e) 
    def fetch(self, groupId: str, userId: str):
        try:
            data: Participant = Participant.query.filter_by(Hash = self.get_hashkey(groupId, userId)).first()
            if (data == None):
                return None
            return data
        except Exception as e:
            raise ParticipantException.WhenPartcipantFetchFailed(e)
        
    def Confirm(self, groupId: str, userId: str):
        try:
            data: Participant = Participant.query.filter_by(Hash = self.get_hashkey(groupId, userId)).first()
            if (data == None):
                raise ParticipantException.WhenParticipantDoesNotExist(groupId, userId)
            data.Confirm_Participant()
            db.session.commit()
        except Exception as e:
            if e.__class__.__base__ != ParticipantException:
                raise ParticipantException.WhenParticipantUpdateFailed(e)
            else:
                raise e
            
    def Block(self, groupId: str, userId: str):
        try:
            data: Participant = Participant.query.filter_by(Hash = self.get_hashkey(groupId, userId)).first()
            if (data == None):
                raise ParticipantException.WhenParticipantDoesNotExist(groupId, userId)
            data.Block_Participant()
            db.session.commit()
        except Exception as e:
            if e.__class__.__base__ != ParticipantException:
                raise ParticipantException.WhenParticipantUpdateFailed(e)
            else:
                raise e
    
    def Block(self, groupId: str, userId: str):
        try:
            data: Participant = Participant.query.filter_by(Hash = self.get_hashkey(groupId, userId)).first()
            if (data == None):
                raise ParticipantException.WhenParticipantDoesNotExist(groupId, userId)
            data.Block_Participant()
            db.session.commit()
        except Exception as e:
            if e.__class__.__base__ != ParticipantException:
                raise ParticipantException.WhenParticipantUpdateFailed(e)
            else:
                raise e
            
    def Unblock(self, groupId: str, userId: str):
        try:
            data: Participant = Participant.query.filter_by(Hash = self.get_hashkey(groupId, userId)).first()
            db.session.delete(data)
            db.session.commit()
        except Exception as e:
            ParticipantException.WhenParticipantDeleteFailed(e)
            
    def Remove(self, groupId: str, userId: str):
        try:
            data: Participant = Participant.query.filter_by(Hash = self.get_hashkey(groupId, userId)).first()
            if (data == None):
                raise ParticipantException.WhenParticipantDoesNotExist(groupId, userId)
            db.session.delete(data)
            db.session.commit()
        except Exception as e:
            if e.__class__.__base__ != ParticipantException:
                raise ParticipantException.WhenParticipantDeleteFailed(e)
            else:
                raise e
                   
    def get_hashkey(self, groupId, userId):
        return f"{userId}_{groupId}"