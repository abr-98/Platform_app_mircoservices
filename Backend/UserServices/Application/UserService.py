from Utility_Module.CheckLoginStatus.StatusException import StatusException
from UserServices.Core.UserExceptions import UserException
from UserServices.Core.User import User
from UserServices.Core.UserResult import UserResult
from UserServices.Infrastructure.UserRepository import UserRepository
from Utility_Module.Elastic.Infrastructure.EntitiesHandler import EntitiesHandler
from Utility_Module.JWTHandler import JWTHandler
from Utility_Module.CheckLoginStatus.StatusRequests import StatusRequests

class UserServices:
    
    def __init__(self):
        self.UserRepository = UserRepository()
        self.ElasticEntityHandler = EntitiesHandler()
    
    def Update(self, field, value, token_in, IP) -> UserResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            self.UserRepository.update(field, value, userId)
            return UserResult.WhenUserFieldIsUpdated(userId, field)
        except Exception as e:
            return UserResult.WhenUserOperationsAreDeniedWithErrors(e)
    def Fetch(self,token_in, IP) -> UserResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            data: User = self.UserRepository.fetch(userId)
            if data == None:
                return UserResult.WhenUserOperationsAreDeniedWithErrors(UserException.WhenUserDoesnotExist())
            return UserResult.WhenUserDataFetched(userId, data)
        except Exception as e:
            return UserResult.WhenUserOperationsAreDeniedWithErrors(e)
        
    def Delete(self, token_in, IP) -> UserResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            self.UserRepository.delete(userId)
            self.ElasticEntityHandler.delete_entity(userId)
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
