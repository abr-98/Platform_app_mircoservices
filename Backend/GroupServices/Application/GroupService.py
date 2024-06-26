import logging
from GroupServices.Core.GroupException import GroupException
from GroupServices.Core.Group import Group
from GroupServices.Core.GroupResult import GroupResult
from GroupServices.Infrastructure.Entites import Entities
from GroupServices.SearchEntityProducer import SearchEntityProducer
from ParticipantServices.Core.Participant import Participant, POSSIBLE_STATUSES
from GroupServices.Infrastructure.GroupRepository import GroupDataRepository
from ParticipantServices.Infrastructure.ParticipantRepository import ParticipantsDataRepository
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton
from Utility_Module.JWTHandler import JWTHandler
from Utility_Module.CheckLoginStatus.StatusException import StatusException
from Utility_Module.CheckLoginStatus.StatusRequests import StatusRequests
import json
from Utility_Module.RedisInfrastructure.CacheRepository import CacheRepository


app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
logger : logging.Logger = app_creater.get_logger()

mq = SearchEntityProducer(logger)
mq.setup()

class GroupServices:
    
    def __init__(self):
        self.GroupRepository = GroupDataRepository()
        self.ParticipantRepository = ParticipantsDataRepository()
        self.CacheRepository = CacheRepository()
        
    def Create(self, group,token_in: str, IP: str) -> GroupResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            group["UserId"] = userId
            group = json.loads(str(group).replace("'",'"'), object_hook= Group.from_json)
            if self.GroupRepository.fetch(group.GroupId) != None:
                return GroupResult.WhenGroupRequirementsFails(GroupException.WhenGroupAlreadyExists(group.GroupId))
            data = self.GroupRepository.fetch(group.GroupId)
            mq.publish("add_request",Entities.From(data.GroupId, data.GroupName, "", "Group"))
            self.GroupRepository.save(group)
            self.CacheRepository.store(group.GroupId, group)
            self.ParticipantRepository.save(Participant(group.Admin, group.GroupId, POSSIBLE_STATUSES.Member.value))
            logger.info(f"Group {data.GroupId} created")
            return GroupResult.WhenGroupIsCreated(group.GroupId, group.GroupName)
        except Exception as e:
            return GroupResult.WhenGroupRequirementsFails(e)
        
    def Fetch(self, groupId: str, token_in: str, IP: str) -> GroupResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            data: Group = self.CacheRepository.fetch(groupId)
            if data == None:
                data: Group = self.GroupRepository.fetch(groupId)
                self.CacheRepository.store(groupId, data)
            if(data== None):
                return GroupResult.WhenGroupRequirementsFails(GroupException.WhenGroupDoesNotExist(groupId))
            logger.info(f"Group {data.GroupId} fetched")
            return GroupResult.WhenGroupIsFetched(data)
        except Exception as e:
            return GroupResult.WhenGroupRequirementsFails(e)
        
    def UpdateInterest(self, groupId: str, interests: str, token_in: str, IP: str) -> GroupResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            data: Group = self.CacheRepository.fetch(groupId)
            if data == None:
                data: Group = self.GroupRepository.fetch(groupId)
                self.CacheRepository.store(groupId, data)
            if not self.__isGroupAdmin__(data, userId):
                return GroupResult.WhenGroupRequirementsFails(GroupException.NonGroupAdminsMakeChanges())
            data = self.GroupRepository.update_interest(groupId,interests)
            self.CacheRepository.store(groupId, data)
            logger.info(f"Group {data.GroupId} updated")
            return GroupResult.WhenGroupIsUpdated(groupId)
        except Exception as e:
            return GroupResult.WhenGroupRequirementsFails(e)
        
    def Delete(self, groupId: str, token_in: str, IP: str) -> GroupResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            data: Group = self.CacheRepository.fetch(groupId)
            if data == None:
                data: Group = self.GroupRepository.fetch(groupId)
                self.CacheRepository.store(groupId, data)
            if not self.__isGroupAdmin__(data, userId):
                return GroupResult.WhenGroupRequirementsFails(GroupException.NonGroupAdminsMakeChanges())
            mq.publish("delete_request",Entities.From(data.GroupId, "", "", "Group"))
            self.GroupRepository.delete(groupId)
            logger.info(f"Group {data.GroupId} deleted")
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
        