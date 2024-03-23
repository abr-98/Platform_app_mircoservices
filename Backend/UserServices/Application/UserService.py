from flask import session
from Utility_Module.CheckLoginStatus.StatusException import StatusException
from Utility_Module.JWTHandler.JWTHandler import JWTgenerator
from Utility_Module.Mailer.MailExceptions import MailException
from UserServices.Core.UserExceptions import UserException
from UserServices.Core.User import User
import random
from UserServices.Core.UserResult import UserResult
from Utility_Module.Mailer.MailerServices import MailServiceInfraSingleton
from UserServices.Infrastructure.UserRepository import UserRepository
from Utility_Module.JWTHandler import JWTHandler
from Utility_Module.CheckLoginStatus.StatusRequests import StatusRequests

class UserServices:
    
    def __init__(self):
        self.UserRepository = UserRepository()
    
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
