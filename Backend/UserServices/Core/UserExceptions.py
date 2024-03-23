class UserException(Exception):
    
    def __init__(self, message: str, ex: Exception):
        self.message : str = message
        self.ex = ex
        
    def __str__(self) -> str:
        return self.message
    
    @staticmethod
    def WhenUserCreationFails(ex : Exception):
        return UserCreationFailed(ex)
    
    @staticmethod
    def WhenUserUpdationFails(ex : Exception):
        return UserUpdateFailed(ex)
    
    @staticmethod
    def WhenUserDoesnotExist():
        return UserDoesNotExist()
    
    @staticmethod
    def WhenUserFetchFails(ex : Exception):
        return UserFetchFailed(ex)
    
    @staticmethod
    def WhenUserDeleteFails(ex : Exception):
        return UserDeleteFailed(ex)
        
    @staticmethod
    def WhenUserVerificationFails(ex : Exception):
        return UserVerificationFailed(ex)
    
    @staticmethod
    def WhenOldPasswordVerificationfails():
        return UserPasswordDoesNotMatch()
    
    @staticmethod
    def WhenUserAlreadyExists():
        return UserIdAlreadyExists()

    @staticmethod
    def WhenUserIsNotVerified():
        return UserNotVerified()
    
class UserCreationFailed(UserException):
    
     def __init__(self, ex: Exception):
        self.message = f"User Creation failed: {str(ex)}"
        super().__init__(self.message,ex)
        
class UserDoesNotExist(UserException):
    
     def __init__(self):
        self.message = f"The given user Does Not exist"
        super().__init__(self.message, None)

class UserUpdateFailed(UserException):
    
     def __init__(self, ex: Exception):
        self.message = f"User Updation failed: {str(ex)}"
        super().__init__(self.message,ex)
        
class UserDeleteFailed(UserException):
    
     def __init__(self, ex: Exception):
        self.message = f"User delete failed: {str(ex)}"
        super().__init__(self.message,ex)
        
class UserFetchFailed(UserException):
    
     def __init__(self, ex: Exception):
        self.message = f"User fetch failed: {str(ex)}"
        super().__init__(self.message,ex)
        
class UserVerificationFailed(UserException):
    
     def __init__(self, ex: Exception):
        self.message = f"User Verification failed: {str(ex)}"
        super().__init__(self.message,ex)

class UserPasswordDoesNotMatch(UserException):
    def __init__(self):
        self.message = f"Password does not match!"
        super().__init__(self.message,None)

class UserIdAlreadyExists(UserException):
    def __init__(self):
        self.message = f"UserId Already exists!"
        super().__init__(self.message,None)
        
class UserNotVerified(UserException):
    def __init__(self):
        self.message = f"User not is not Verified. Please verify with the OTP from mail!"
        super().__init__(self.message,None)