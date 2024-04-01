class EntityException(Exception):
    
    def __init__(self, message: str,ex: Exception):
        self.message : str = message
        self.ex = ex
        
    def __str__(self) -> str:
        return self.message
    
    @staticmethod
    def WhenEntityNotPresent(searchValue):
        return EntityNotPresent(searchValue)
    
    @staticmethod
    def WhenEntitySearchFailed(ex: Exception):
        return EntitySearchFailed(ex)
    
    
class EntityNotPresent(EntityException):
    
    def __init__(self, searchValue):
        self.message = f"{searchValue} is not present"
        super().__init__(self.message, None)
    
class EntitySearchFailed(EntityException):
    
    def __init__(self, ex: Exception):
        self.message = f"Entity Search Failed {str(ex)}"
        super().__init__(self.message, None)
    