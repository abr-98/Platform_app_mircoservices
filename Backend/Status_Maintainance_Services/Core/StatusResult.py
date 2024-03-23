from Status_Maintainance_Services.Core.Status import Status


class StatusResult:
    
    def __init__(self, UserId, IP, Message):
        self.UserId = UserId
        self.IP = IP
        self.Message = Message
        
    @staticmethod
    def WhenLoginIsCreated(UserId, IP):
        return LoginCreated(UserId, IP)
    
    @staticmethod
    def WhenLoginDataFetched(status: Status):
        return LoginDataFetched(status)
    
    @staticmethod
    def WhenLoggedOut(UserId, IP):
        return LogOut(UserId, IP)
    
    @staticmethod 
    def WhenStatusOperationsAreDeniedWithErrors(ex : Exception):
        return StatusOperationDenied(ex)
    
class LoginCreated(StatusResult):
    
    def __init__(self, UserId, IP):
        self.message = f"User {UserId} logged in from {IP}"
        super().__init__(UserId, IP, self.message)
        
class LoginDataFetched(StatusResult):
    
    def __init__(self, Status: Status):
        self.message = f"Status: {Status.__dict__}"
        super().__init__(Status.UserId, Status.IP, self.message)
    

class LogOut(StatusResult):
    
    def __init__(self, UserId, IP):
        self.message = f"User {UserId} logged out from {IP}"
        super().__init__(UserId, IP, self.message)
        
class StatusOperationDenied(StatusResult):
    
    def __init__(self,ex : Exception):
        self.ex = ex
        self.message = str(ex)
        super().__init__(None, None, self.message)