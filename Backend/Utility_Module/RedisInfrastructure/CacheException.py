class CatchException(Exception):
    
    def __init__(self, message: str, ex: Exception):
        self.message : str = message
        self.ex = ex
        
    def __str__(self) -> str:
        return self.message
    
    @staticmethod
    def WhenCacheOperationFails(ex: Exception):
        return CacheOperationFailed(ex)
    
class CacheOperationFailed(CatchException):
    
    
     def __init__(self, ex: Exception):
        self.message = f"cache operation failed: {str(ex)}"
        super().__init__(self.message,ex)