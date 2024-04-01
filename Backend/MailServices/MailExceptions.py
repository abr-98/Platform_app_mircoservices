class MailException(Exception):
    
    def __init__(self, message: str):
        self.message : str = message
        
    def __str__(self) -> str:
        return self.message
    
    @staticmethod
    def WhenMailDispatchFails(ex : Exception):
        return MailDispatchFailed(ex)

class MailDispatchFailed(MailException):
    
     def __init__(self, ex: Exception):
        self.message = f"Mail Dispatch failed: {str(ex)}"
        self.ex = ex
        super().__init__(self.message)