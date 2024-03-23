from UserServices.Core.User import User


class UserResult:
    
    def __init__(self, UserId, UserName, Message):
        super().__init__()
        self.UserId = UserId
        self.UserName = UserName
        self.Message = Message
        
    @staticmethod
    def WhenUserIsCreated(UserId, UserName):
        return UserCreated(UserId, UserName)
    
    @staticmethod
    def WhenUserDataFetched(UserId, user):
        return UserDataFetched(UserId, user)
    
    @staticmethod
    def WhenUserFieldIsUpdated(UserId, field):
        return UserFieldUpdated(UserId, field)
    
    @staticmethod
    def WhenUserIsDeleted(UserId):
        return UserDataDeleted(UserId)
    
    @staticmethod
    def WhenUserIsVerified(UserId):
        return UserVerified(UserId)
    
    @staticmethod
    def WhenUserIsRecovered(UserId):
        return UserAccountRecovered(UserId)
    
    @staticmethod
    def WhenUserIsLoggedIn(UserId, Token):
        return UserLoggedIn(UserId, Token)
    
    @staticmethod
    def WhenUserIsLoggedOut(UserId):
        return UserLoggedOut(UserId)
    
    @staticmethod 
    def WhenUserOperationsAreDeniedWithErrors(ex : Exception):
        return UserOperationDenied(ex)
        
    
class UserCreated(UserResult):
    
    def __init__(self, UserId, UserName):
        self.message = f"User {UserName} is created with Id {UserId}"
        super().__init__(UserId, UserName, self.message)

class UserFieldUpdated(UserResult):
    
    def __init__(self, UserId, field):
        self.message = f"Field {field} is updated for User {UserId}"
        super().__init__(UserId, "", self.message)
        self.field = field
        
class UserDataFetched(UserResult):
    
    def __init__(self, UserId, user: User):
        self.message = f"Details: Name: {user.__dict__}"
        super().__init__(UserId, "", self.message)
        self.user = user
        
class UserDataDeleted(UserResult):
    
    def __init__(self, UserId):
        self.message =f"Account for {UserId} is deleted"
        super().__init__(UserId, "", self.message)
        
class UserVerified(UserResult):
    
    def __init__(self, UserId):
        self.message=f"User {UserId} is Verified"
        super().__init__(UserId, "", self.message)
        
class UserAccountRecovered(UserResult):
    
    def __init__(self, UserId):
        self.message=f"User {UserId} is Recovered"
        super().__init__(UserId, "", self.message)
        
class UserLoggedIn(UserResult):
    
    def __init__(self, UserId, token):
        self.message = "{"+f"UserId: {UserId},Token: {token}" +"}" 
        super().__init__(UserId, "", self.message)
        
class UserLoggedOut(UserResult):
    
    def __init__(self, UserId):
        self.message = f"User {UserId} is logged out" 
        super().__init__(UserId, "", self.message)
        
class UserOperationDenied(UserResult):
    
    def __init__(self,ex : Exception):
        super().__init__("","", None)
        self.ex = ex
        self.message = str(ex)
        
        
        
         
        
    