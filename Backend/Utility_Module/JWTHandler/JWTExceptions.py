class JWTExceptions(Exception):
    
    def __init__(self, message: str):
        self.message : str = message
        
    def __str__(self) -> str:
        return self.message
    
    @staticmethod
    def WhenTokenValidationFails(ex : Exception):
        return TokenValidationFailed(ex)

class TokenValidationFailed(JWTExceptions):
    
     def __init__(self, ex: Exception):
        self.message = f"Token Validation Failed: {str(ex)}"
        self.ex = ex
        super().__init__(self.message)