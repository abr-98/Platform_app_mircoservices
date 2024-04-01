class PostException(Exception):
    
    def __init__(self, message: str, ex: Exception):
        self.message : str = message
        self.ex = ex
        
    def __str__(self) -> str:
        return self.message
    
    @staticmethod 
    def WhenPostCreationFails(ex: Exception):
        return PostCreationFailed(ex)
    
    @staticmethod 
    def WhenPostFetchFails(ex: Exception):
        return PostFetchFailed(ex)
    
    @staticmethod 
    def WhenPostDeletionFails(ex: Exception):
        return PostDeleteFailed(ex)
    
class PostCreationFailed(PostException):
    
     def __init__(self, ex: Exception):
        self.message = f"Post Creation failed: {str(ex)}"
        super().__init__(self.message,ex)
        
class PostFetchFailed(PostException):
    
     def __init__(self, ex: Exception):
        self.message = f"Post fetch failed: {str(ex)}"
        super().__init__(self.message,ex)
        
class PostDeleteFailed(PostException):
    
     def __init__(self, ex: Exception):
        self.message = f"Post deletion failed: {str(ex)}"
        super().__init__(self.message,ex)