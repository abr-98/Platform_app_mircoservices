from GroupServices.Core.GroupException import GroupException
from ParticipantServices.Core.ParticipantException import ParticipantException
from ParticipantServices.Core.ParticipantResult import ParticipantResult
from GroupServices.Core.Group import Group
from GroupServices.Infrastructure.GroupRepository import GroupDataRepository
from ParticipantServices.Infrastructure.ParticipantRepository import ParticipantsDataRepository
from ParticipantServices.Core.Participant import Participant, POSSIBLE_STATUSES
from Utility_Module.JWTHandler import JWTHandler
from Utility_Module.CheckLoginStatus.StatusException import StatusException
from Utility_Module.CheckLoginStatus.StatusRequests import StatusRequests


class ParticipantServices:
    
    def __init__(self):
        self.ParticipantRepository = ParticipantsDataRepository()
        self.GroupRepository = GroupDataRepository()
        
    def ParticipantRequestToAdd(self, token_in, IP, groupId) -> ParticipantResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            if not self.__IsNotBlocked__(userId,groupId):
                return ParticipantResult.WhenParticipantRequestFail(ParticipantException.WhenParticipantIsBlocked(groupId,userId))
            
            if self.ParticipantRepository.fetch(groupId, userId) is not None:
                return ParticipantResult.WhenParticipantRequestFail(ParticipantException.WhenParticipantAlreadyExists(groupId,userId))
        
            self.ParticipantRepository.save(Participant(userId, groupId, POSSIBLE_STATUSES.Requested.value))
            return ParticipantResult.WhenParticipantIsCreated(groupId,userId)
        except Exception as e:
            return ParticipantResult.WhenParticipantRequestFail(e)
        
    def AdminRequestToAdd(self, token_in, IP, groupId, userId) -> ParticipantResult:
        try:
            admin = self.check_login_and_token(token_in, IP)
            data: Group = self.GroupRepository.fetch(groupId)
            if not self.__isGroupAdmin__(data, admin):
                return ParticipantResult.WhenParticipantRequestFail(GroupException.NonGroupAdminsMakeChanges())
            
            if not self.__IsNotBlocked__(userId,groupId):
                return ParticipantResult.WhenParticipantRequestFail(ParticipantException.WhenParticipantIsBlocked(groupId,userId))
            
            if self.ParticipantRepository.fetch(groupId, userId) is not None:
                return ParticipantResult.WhenParticipantRequestFail(ParticipantException.WhenParticipantAlreadyExists(groupId,userId))
        
            self.ParticipantRepository.save(Participant(userId, groupId, POSSIBLE_STATUSES.Add_request_pending.value))
            return ParticipantResult.WhenParticipantIsCreated(groupId,userId)
        except Exception as e:
            return ParticipantResult.WhenParticipantRequestFail(e)
    
    def GetParticipant(self, token_in, IP, groupId) -> ParticipantResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            data: Participant = self.ParticipantRepository.fetch(groupId, userId)
            
            if data is None:
                return ParticipantResult.WhenParticipantRequestFail(ParticipantException.WhenParticipantDoesNotExist(groupId, userId))
            
            return ParticipantResult.WhenParticipantIsFetched(data)
        except Exception as e:
            return ParticipantResult.WhenParticipantRequestFail(e)
        
    def Confirm(self, token_in, IP, groupId) -> ParticipantResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            self.ParticipantRepository.Confirm(groupId, userId) 
            return ParticipantResult.WhenParticipantIsConfirmed(groupId, userId)
        except Exception as e:
            return ParticipantResult.WhenParticipantRequestFail(e)
        
    def ConfirmByAdmin(self, token_in, IP, groupId, userId) -> ParticipantResult:
        try:
            admin = self.check_login_and_token(token_in, IP)
            data: Group = self.GroupRepository.fetch(groupId)
            if not self.__isGroupAdmin__(data, admin):
                return ParticipantResult.WhenParticipantRequestFail(GroupException.NonGroupAdminsMakeChanges())
            
            self.ParticipantRepository.Confirm(groupId, userId) 
            return ParticipantResult.WhenParticipantIsConfirmed(groupId, userId)
        except Exception as e:
            return ParticipantResult.WhenParticipantRequestFail(e)
        
    def Block(self, token_in, IP, groupId, userId) -> ParticipantResult:
        try:
            admin = self.check_login_and_token(token_in, IP)
            data: Group = self.GroupRepository.fetch(groupId)
            if not self.__isGroupAdmin__(data, admin):
                return ParticipantResult.WhenParticipantRequestFail(GroupException.NonGroupAdminsMakeChanges())
            
            self.ParticipantRepository.Block(groupId, userId) 
            return ParticipantResult.WhenParticipantIsBlocked(groupId, userId)
        except Exception as e:
            return ParticipantResult.WhenParticipantRequestFail(e)
        
    def Unblock(self, token_in, IP, groupId, userId) -> ParticipantResult:
        try:
            admin = self.check_login_and_token(token_in, IP)
            data: Group = self.GroupRepository.fetch(groupId)
            if not self.__isGroupAdmin__(data, admin):
                return ParticipantResult.WhenParticipantRequestFail(GroupException.NonGroupAdminsMakeChanges())
                        
            self.ParticipantRepository.Unblock(groupId, userId) 
            return ParticipantResult.WhenParticipantIsUnblocked(groupId, userId)
        except Exception as e:
            return ParticipantResult.WhenParticipantRequestFail(e)
        
    def Remove(self, token_in, IP, groupId, userId) -> ParticipantResult:
        try:
            admin = self.check_login_and_token(token_in, IP)
            data: Group = self.GroupRepository.fetch(groupId)
            if not self.__isGroupAdmin__(data, admin):
                return ParticipantResult.WhenParticipantRequestFail(GroupException.NonGroupAdminsMakeChanges())
                       
            self.ParticipantRepository.Remove(groupId, userId) 
            return ParticipantResult.WhenParticipantIsRemoved(groupId, userId)
        except Exception as e:
            return ParticipantResult.WhenParticipantRequestFail(e)
        
    def Leave(self, token_in, IP, groupId) -> ParticipantResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            self.ParticipantRepository.Remove(groupId, userId) 
            return ParticipantResult.WhenParticipantIsRemoved(groupId, userId)
        except Exception as e:
            return ParticipantResult.WhenParticipantRequestFail(e)
        
        
    def __IsNotBlocked__(self,userId, groupId):
        data: Participant = self.ParticipantRepository.fetch(groupId,userId)
        return data == None or int(data.Status) != POSSIBLE_STATUSES.Blocked.value
    
    def __isGroupAdmin__(self,data: Group, userId: str):
        if( data.Admin.find(',') != -1):
            admin = data.Admin.split(',')
            if userId in admin:
                return True
        else:
            if userId == data.Admin:
                return True
        
        return False
    
    def check_login_and_token(self, token_in, IP):
        token = JWTHandler.JWTgenerator.ValidateToken(token_in)
        userId = token["Id"]
        code = StatusRequests.FetchLogin(userId, IP)
        if code != 200:
            raise StatusException.WhenUserNotLoggedIn()
        return userId   