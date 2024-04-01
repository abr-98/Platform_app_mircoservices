import logging
import random
from UserServices.Core.User import User
from UserServices.Core.UserExceptions import UserException
from UserServices.Core.UserResult import UserResult
from UserServices.Infrastructure.Entites import Entities
from UserServices.Infrastructure.Mail import Mail
from UserServices.Infrastructure.UserRepository import UserRepository
from UserServices.MailEventProducer import MailEventProducer
from UserServices.SearchEntityProducer import SearchEntityProducer
from Utility_Module.CheckLoginStatus.StatusRequests import StatusRequests
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton
from Utility_Module.JWTHandler.JWTHandler import JWTgenerator

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
logger : logging.Logger = app_creater.get_logger()

mq_elastic = SearchEntityProducer(logger)
mq_elastic.setup()
mq_mail = MailEventProducer(logger)
mq_mail.setup()


class RegistrationServices:
    
    def __init__(self):
        self.UserRepository = UserRepository()
        
    def Persist(self, user: User) -> UserResult:
        try:
            data = self.UserRepository.fetch(user.UserId)
            if data != None:
                return UserResult.WhenUserOperationsAreDeniedWithErrors(UserException.WhenUserAlreadyExists())
            otp: str = self.CreateOTP()
            message, subject =self.CreateSetPasswordMessage(otp, user.UserId)
            mq_mail.publish("mail_requested", Mail(user.Email,message, subject))
            user.updateValue("Password", otp)    
            mq_elastic.publish("add_request", Entities.From(user.UserId, user.Name, "", "Person"))
            self.UserRepository.save(user)
            return UserResult.WhenUserIsCreated(user.UserId, user.Name)
        except Exception as e:
            return UserResult.WhenUserOperationsAreDeniedWithErrors(e)
        
    def Login(self, userId, password,ip) -> UserResult:
        try:
            data : User = self.UserRepository.fetch(userId)
            if data == None:
                return UserResult.WhenUserOperationsAreDeniedWithErrors(UserException.WhenUserDoesnotExist())
            if not data.is_authenticated():
                return UserResult.WhenUserOperationsAreDeniedWithErrors(UserException.WhenUserIsNotVerified())
            if data.checkPassword(password):
                code = StatusRequests.CreateLogin(userId, ip)
                if code != 200:
                    raise UserException.WhenUserCreationFails(Exception("Create Login for device fails"))
                return UserResult.WhenUserIsLoggedIn(userId,JWTgenerator.generateToken(data.UserId, data.Name))
            else:
                return UserResult.WhenUserOperationsAreDeniedWithErrors(UserException.WhenOldPasswordVerificationfails())
        except Exception as e:
            return UserResult.WhenUserOperationsAreDeniedWithErrors(e)
        
    def Recover(self, userEmail) -> UserResult:
        try:
            data: User = self.UserRepository.fetchByField("Email",userEmail)
            if data == None:
                return UserResult.WhenUserOperationsAreDeniedWithErrors(UserException.WhenUserDoesnotExist())
            otp: str = self.CreateOTP()
            message, subject =self.CreateSetPasswordMessage(otp, data.UserId)
            mq_mail.publish("mail_requested", Mail(userEmail, message, subject))
            self.UserRepository.update("Password", otp, data.UserId)
            return UserResult.WhenUserIsRecovered(data.UserId)
        except Exception as e:
            return UserResult.WhenUserOperationsAreDeniedWithErrors(e)
        
    def Verify(self, userId, OTP, Password) -> UserResult:
        try:
            data : User = self.UserRepository.fetch(userId)
            if not data.checkPassword(OTP):
                return UserResult.WhenUserOperationsAreDeniedWithErrors(UserException.WhenOldPasswordVerificationfails())
            self.UserRepository.update("Password", Password, userId)
            self.UserRepository.Verify(userId)
            return UserResult.WhenUserIsVerified(userId)
        except Exception as e:
            return UserResult.WhenUserOperationsAreDeniedWithErrors(e)
        
        
    def CreateSetPasswordMessage(self, OTP: str, UserId: str):
        return f"Dear {UserId}, \nPlease reset your password, to a new password. Your current Password is {OTP}", "Account Password"
    
    def CreateOTP(self):
        return str(random.randint(100000, 999999))
    
            