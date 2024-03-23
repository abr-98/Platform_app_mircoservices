from Status_Maintainance_Services.Core.Status import Status
from Status_Maintainance_Services.Core.OnlineStatusException import OnlineStatusException
from Status_Maintainance_Services.Core.StatusResult import StatusResult
from Status_Maintainance_Services.Infrastructure.StatusRepository import StatusRepository


class StatusServices:
    
    def __init__(self):
        self.StatusRepository = StatusRepository()
        
    def CreateLogin(self,status: Status):
        try:
            self.StatusRepository.save(status)
            return StatusResult.WhenLoginIsCreated(status.UserId, status.IP)
        except Exception as e:
            return StatusResult.WhenStatusOperationsAreDeniedWithErrors(e)
        
    def FetchLogin(self, userId, IP):
        try:
            data = self.StatusRepository.fetch(userId, IP)
            
            if data == None:
                return StatusResult.WhenStatusOperationsAreDeniedWithErrors(OnlineStatusException.WhenUserNotLoggedIn(userId))
            return StatusResult.WhenLoginDataFetched(data)
        except Exception as e:
            return StatusResult.WhenStatusOperationsAreDeniedWithErrors(e)
        
    def Logout(self, userId, IP):
        try:
            self.StatusRepository.delete(userId, IP)
            return StatusResult.WhenLoggedOut(userId, IP)
        except Exception as e:
            return StatusResult.WhenStatusOperationsAreDeniedWithErrors(e)
               