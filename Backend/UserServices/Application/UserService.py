import logging
from UserServices.Infrastructure.Entites import Entities
from UserServices.SearchEntityProducer import SearchEntityProducer
from Utility_Module.CheckLoginStatus.StatusException import StatusException
from UserServices.Core.UserExceptions import UserException
from UserServices.Core.User import User
from UserServices.Core.UserResult import UserResult
from UserServices.Infrastructure.UserRepository import UserRepository
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton
from Utility_Module.JWTHandler import JWTHandler
from Utility_Module.CheckLoginStatus.StatusRequests import StatusRequests
from Utility_Module.RedisInfrastructure.CacheRepository import CacheRepository

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
logger : logging.Logger = app_creater.get_logger()

mq_elastic = SearchEntityProducer(logger)
mq_elastic.setup()

class UserServices:
    
    def __init__(self):
        self.UserRepository = UserRepository()
        self.CacheHandler = CacheRepository()
    
    def Update(self, field, value, token_in, IP) -> UserResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            data = self.UserRepository.update(field, value, userId)
            self.CacheHandler.store(userId,data)
            return UserResult.WhenUserFieldIsUpdated(userId, field)
        except Exception as e:
            return UserResult.WhenUserOperationsAreDeniedWithErrors(e)
        
    def Fetch(self,token_in, IP) -> UserResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            data = self.CacheHandler.fetch(userId)
            if data == None:
                data: User = self.UserRepository.fetch(userId)
                self.CacheHandler.store(userId,data)
            if data == None:
                return UserResult.WhenUserOperationsAreDeniedWithErrors(UserException.WhenUserDoesnotExist())
            return UserResult.WhenUserDataFetched(userId, data)
        except Exception as e:
            return UserResult.WhenUserOperationsAreDeniedWithErrors(e)
        
    def Delete(self, token_in, IP) -> UserResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            self.UserRepository.delete(userId)
            mq_elastic.publish("delete_request", Entities.From(userId, "", "", "Person"))
            return UserResult.WhenUserIsDeleted(userId)
        except Exception as e:
            return UserResult.WhenUserOperationsAreDeniedWithErrors(e)
        
    def Logout(self, token_in, IP) -> UserResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            code = StatusRequests.Delete(userId, IP)
            if code != 200:
                raise UserException.WhenUserUpdationFails(Exception("Logout Operation Failed"))
            return UserResult.WhenUserIsLoggedOut(userId)
        except Exception as e:
            return UserResult.WhenUserOperationsAreDeniedWithErrors(e)
            
        
    def check_login_and_token(self, token_in, IP):
        token = JWTHandler.JWTgenerator.ValidateToken(token_in)
        userId = token["Id"]
        code = StatusRequests.FetchLogin(userId, IP)
        if code != 200:
            raise StatusException.WhenUserNotLoggedIn()
        return userId    
