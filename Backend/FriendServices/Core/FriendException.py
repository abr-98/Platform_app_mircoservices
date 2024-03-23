class FriendException(Exception):
    
    def __init__(self, message: str,ex: Exception):
        self.message : str = message
        self.ex = ex
        
    def __str__(self) -> str:
        return self.message
    
    @staticmethod
    def WhenFriendRequestCreationFails(ex: Exception):
        return FriendRequestCreationFailed(ex)
    
    @staticmethod
    def WhenRequestedUserIsBlocked(userId, friendId):
        return RequestedUserIsBlocked(userId,friendId)
    
    @staticmethod
    def WhenRequestStateChangeFails(ex: Exception):
        return RequestStateChangeFailed(ex)
    
    @staticmethod
    def WhenFriendRemovalFails(ex: Exception):
        return FriendRemovalFailed(ex)
    
    @staticmethod
    def WhenFriendDataFetchFails(ex: Exception):
        return FriendDataFetched(ex)
    
class FriendRequestCreationFailed(FriendException):
    
     def __init__(self, ex: Exception):
        self.message = f"Friend Request Creation failed: {str(ex)}"
        super().__init__(self.message, ex)
        
class RequestedUserIsBlocked(FriendException):
    
     def __init__(self, UserId, FriendId):
        self.message = f"{UserId} is blocked for {FriendId}"
        super().__init__(self.message, None)
        
class RequestStateChangeFailed(FriendException):
    
     def __init__(self, ex:Exception):
        self.message = f"Friend State Change Failed {str(ex)}"
        super().__init__(self.message, ex)
        
class FriendRemovalFailed(FriendException):
    
     def __init__(self, ex: Exception):
        self.message = f"Friend Removal failed: {str(ex)}"
        super().__init__(self.message,ex)
        
class FriendDataFetched(FriendException):
    
     def __init__(self, ex: Exception):
        self.message = f"Friend fetch failed: {str(ex)}"
        super().__init__(self.message, ex)
    