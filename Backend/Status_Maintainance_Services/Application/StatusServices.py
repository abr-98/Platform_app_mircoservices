import logging
from Status_Maintainance_Services.Core.Status import Status
from Status_Maintainance_Services.Core.OnlineStatusException import OnlineStatusException
from Status_Maintainance_Services.Core.StatusResult import StatusResult
from Status_Maintainance_Services.Infrastructure.StatusRepository import StatusRepository
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
logger : logging.Logger = app_creater.get_logger()


class StatusServices:
    
    def __init__(self):
        self.StatusRepository = StatusRepository()
        
    def CreateLogin(self,status: Status):
        try:
            self.StatusRepository.save(status)
            logger.info("User Login record created")
            return StatusResult.WhenLoginIsCreated(status.UserId, status.IP)
        except Exception as e:
            return StatusResult.WhenStatusOperationsAreDeniedWithErrors(e)
        
    def FetchLogin(self, userId, IP):
        try:
            data = self.StatusRepository.fetch(userId, IP)
            logger.info("User Login record fetched")
            if data == None:
                return StatusResult.WhenStatusOperationsAreDeniedWithErrors(OnlineStatusException.WhenUserNotLoggedIn(userId))
            return StatusResult.WhenLoginDataFetched(data)
        except Exception as e:
            return StatusResult.WhenStatusOperationsAreDeniedWithErrors(e)
        
    def Logout(self, userId, IP):
        try:
            self.StatusRepository.delete(userId, IP)
            logger.info("User Login record removed")
            return StatusResult.WhenLoggedOut(userId, IP)
        except Exception as e:
            return StatusResult.WhenStatusOperationsAreDeniedWithErrors(e)
               