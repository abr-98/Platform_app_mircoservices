from FriendServices.Core.Friend import Friend


class FriendResult():
    
    def __init__(self, UserId, FriendId, Message):
        super().__init__()
        self.UserId = UserId
        self.FriendId = FriendId
        self.Message = Message
        
    
    @staticmethod
    def WhenFriendRequestSent(UserId, FriendId):
        return FriendRequestSent(UserId, FriendId)
    
    @staticmethod
    def WhenFriendConfirmed(UserId, FriendId):
        return FriendConfirmed(UserId, FriendId)
    
    @staticmethod
    def WhenFriendBlocked(UserId, FriendId):
        return FriendBlocked(UserId, FriendId)
    
    @staticmethod
    def WhenFriendRequestFailed(ex : Exception):
        return FriendRequestFailed(ex)
    
    @staticmethod
    def WhenFriendRemoved(UserId, FriendId):
        return FriendRemoved(UserId, FriendId)
    
    @staticmethod
    def WhenFriendIsFetched(Friend : Friend):
        return FriendDataFetched(Friend)
    
    @staticmethod
    def WhenFriendIsUnblocked(UserId, FriendId):
        return FriendUnblocked(UserId, FriendId)
    
    
class FriendRequestSent(FriendResult):
    
    def __init__(self, UserId, FriendId):
        self.message = f"Connection Request Sent For User {FriendId} From {UserId}"
        super().__init__(UserId, FriendId, self.message)

class FriendConfirmed(FriendResult):
    
    def __init__(self, UserId, FriendId):
        self.message = f"{UserId} and {FriendId} are connected"
        super().__init__(UserId, FriendId, self.message)
        
class FriendBlocked(FriendResult):
    
    def __init__(self, UserId, FriendId):
        self.message = f"User {FriendId} is blocked by {UserId}"
        super().__init__(UserId, FriendId, self.message)
        
class FriendRequestFailed(FriendResult):
    
    def __init__(self, ex : Exception):
        super().__init__("", "",None)
        self.message = f"The request could not be fulfilled {str(ex)}"
        self.ex = ex
        
class FriendRemoved(FriendResult):
    
    def __init__(self, UserId, FriendId):
        self.message = f"{UserId} and {FriendId} are disconnected"
        super().__init__(UserId, FriendId, self.message)
        
class FriendDataFetched(FriendResult):
    
    def __init__(self, Friend : Friend):
        self.message = f"Friend data fetched {Friend.__dict__}"
        super().__init__("", "", self.message)
        self.Friend = Friend
        
class FriendUnblocked(FriendResult):
    
    def __init__(self, UserId, FriendId):
        self.message = f"{UserId} has unblocked {FriendId}"
        super().__init__(UserId, FriendId, self.message)
        