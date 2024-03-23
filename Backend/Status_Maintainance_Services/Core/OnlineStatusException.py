class OnlineStatusException(Exception):
    
    def __init__(self, message: str, ex: Exception):
        self.message : str = message
        self.ex = ex
        
    def __str__(self) -> str:
        return self.message
    
    @staticmethod
    def WhenStatusChangeFails(ex : Exception):
        return StatusChangeFailed(ex)
    
    @staticmethod
    def WhenStatusFetchFails(ex : Exception):
        return StatusFetchFailed(ex)
    
    @staticmethod
    def WhenUserNotLoggedIn(userId: str):
        return LoginDoesNotExist(userId)
    
class StatusChangeFailed(OnlineStatusException):
    
     def __init__(self, ex: Exception):
        self.message = f"Status change failed: {str(ex)}"
        super().__init__(self.message,ex)
        
class LoginDoesNotExist(OnlineStatusException):
    
     def __init__(self, userId: str):
        self.message = f"User {userId} is not logged in from the device"
        super().__init__(self.message,None)
        
        
class StatusFetchFailed(OnlineStatusException):
    
     def __init__(self, ex: Exception):
        self.message = f"Status fetch failed: {str(ex)}"
        super().__init__(self.message,ex)