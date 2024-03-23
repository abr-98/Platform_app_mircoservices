class StatusException(Exception):
    
    def __init__(self, message: str, ex: Exception):
        self.message : str = message
        self.ex = ex
        
    def __str__(self) -> str:
        return self.message
    
    
    @staticmethod
    def WhenUserNotLoggedIn():
        return UserNotLoggedIn()
    
    
class UserNotLoggedIn(StatusException):
    def __init__(self):
        self.message = f"User not logged in!"
        super().__init__(self.message,None)