class InteractionException(Exception):
    
    def __init__(self, message: str,ex: Exception):
        self.message : str = message
        self.ex = ex
        
    def __str__(self) -> str:
        return self.message
    
    @staticmethod
    def WhenInterationOperationFailed(ex: Exception):
        return InteractionOperaitionFailed(ex)
        
    
    
class InteractionOperaitionFailed(InteractionException):
    
     def __init__(self, ex: Exception):
        self.message = f"Interaction Event Creation failed: {str(ex)}"
        super().__init__(self.message,ex)