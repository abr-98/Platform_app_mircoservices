class BlobException(Exception):
    
    def __init__(self, message: str, ex: Exception):
        self.message : str = message
        self.ex = ex
        
    def __str__(self) -> str:
        return self.message
    
    @staticmethod
    def WhenBlobOperationFails(ex: Exception):
        return BlobOperationFailed(ex)
    
class BlobOperationFailed(BlobException):
    
    
     def __init__(self, ex: Exception):
        self.message = f"Blob operation failed: {str(ex)}"
        super().__init__(self.message,ex)