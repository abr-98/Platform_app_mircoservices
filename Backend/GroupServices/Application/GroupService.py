from GroupServices.Core.GroupException import GroupException
from GroupServices.Core.Group import Group
from GroupServices.Core.GroupResult import GroupResult
from ParticipantServices.Core.Participant import Participant, POSSIBLE_STATUSES
from GroupServices.Infrastructure.GroupRepository import GroupDataRepository
from ParticipantServices.Infrastructure.ParticipantRepository import ParticipantsDataRepository
from Utility_Module.JWTHandler import JWTHandler
from Utility_Module.CheckLoginStatus.StatusException import StatusException
from Utility_Module.CheckLoginStatus.StatusRequests import StatusRequests
import json


class GroupServices:
    
    def __init__(self):
        self.GroupRepository = GroupDataRepository()
        self.ParticipantRepository = ParticipantsDataRepository()
        
    def Create(self, group,token_in: str, IP: str) -> GroupResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            group["UserId"] = userId
            data = json.loads(str(group).replace("'",'"'), object_hook= Group.from_json)
            data: Group = self.GroupRepository.fetch(group.GroupId)
            if(data!= None):
                return GroupResult.WhenGroupRequirementsFails(GroupException.WhenGroupAlreadyExists(group.GroupId))
            self.GroupRepository.save(group)
            self.ParticipantRepository.save(Participant(group.Admin, group.GroupId, POSSIBLE_STATUSES.Member.value))
            return GroupResult.WhenGroupIsCreated(group.GroupId, group.GroupName)
        except Exception as e:
            return GroupResult.WhenGroupRequirementsFails(e)
        
    def Fetch(self, groupId: str, token_in: str, IP: str) -> GroupResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            data: Group = self.GroupRepository.fetch(groupId)
            if(data== None):
                return GroupResult.WhenGroupRequirementsFails(GroupException.WhenGroupDoesNotExist(groupId))
            return GroupResult.WhenGroupIsFetched(data)
        except Exception as e:
            return GroupResult.WhenGroupRequirementsFails(e)
        
    def UpdateInterest(self, groupId: str, interests: str, token_in: str, IP: str) -> GroupResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            data: Group = self.GroupRepository.fetch(groupId)
            if not self.__isGroupAdmin__(data, userId):
                return GroupResult.WhenGroupRequirementsFails(GroupException.NonGroupAdminsMakeChanges())
            self.GroupRepository.update_interest(groupId,interests)
            return GroupResult.WhenGroupIsUpdated(groupId)
        except Exception as e:
            return GroupResult.WhenGroupRequirementsFails(e)
        
    def Delete(self, groupId: str, token_in: str, IP: str) -> GroupResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            data: Group = self.GroupRepository.fetch(groupId)
            if not self.__isGroupAdmin__(data, userId):
                return GroupResult.WhenGroupRequirementsFails(GroupException.NonGroupAdminsMakeChanges())
            self.GroupRepository.delete(groupId)
            return GroupResult.WhenGroupIsDeleted(groupId)
        except Exception as e:
            return GroupResult.WhenGroupRequirementsFails(e)
        
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
        