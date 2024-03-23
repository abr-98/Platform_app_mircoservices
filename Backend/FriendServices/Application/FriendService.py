from FriendServices.Core.FriendException import FriendException
from FriendServices.Core.Friend import Friend,POSSIBLE_STATUSES
from FriendServices.Core.FriendResult import FriendResult
from FriendServices.Infrastructure.FriendRepository import FriendRepository
from Utility_Module.JWTHandler import JWTHandler
from Utility_Module.CheckLoginStatus.StatusException import StatusException
from Utility_Module.CheckLoginStatus.StatusRequests import StatusRequests

class FriendService:
    
    def __init__(self):
        self.FriendRepository = FriendRepository()
        
    def AddFriend(self, token_in, IP, friendId) -> FriendResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            if (not self.__IsNotBlocked__(userId,friendId)) or (not self.__IsNotBlocked__(friendId, userId)):
                return FriendResult.WhenFriendRequestFailed(FriendException.WhenRequestedUserIsBlocked(userId, friendId))
            self.FriendRepository.addFriend(userId,friendId)
            return FriendResult.WhenFriendRequestSent(userId, friendId)
        except Exception as e:
            return FriendResult.WhenFriendRequestFailed(e)
        
    def ConfirmFriend(self, token_in, IP, friendId) -> FriendResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            self.FriendRepository.confirmFriend(userId,friendId)
            return FriendResult.WhenFriendConfirmed(userId, friendId)
        except Exception as e:
            return FriendResult.WhenFriendRequestFailed(e)
            
    def BlockFriend(self, token_in, IP, friendId) -> FriendResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            self.FriendRepository.blockFriend(userId,friendId)
            return FriendResult.WhenFriendBlocked(userId, friendId)
        except Exception as e:
            return FriendResult.WhenFriendRequestFailed(e)
        
    def RemoveFriend(self, token_in, IP, friendId) -> FriendResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            self.FriendRepository.removeFriend(userId, friendId)
            return FriendResult.WhenFriendRemoved(userId, friendId)
        except Exception as e:
            return FriendResult.WhenFriendRequestFailed(e)
    
    def UnblockFriend(self, token_in, IP, friendId) -> FriendResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            self.FriendRepository.unblockFriend(userId, friendId)
            return FriendResult.WhenFriendIsUnblocked(userId, friendId)
        except Exception as e:
            return FriendResult.WhenFriendRequestFailed(e)
    
    
    def __IsNotBlocked__(self, passed_userId, passed_friendId):
        data: Friend = self.FriendRepository.fetch(passed_userId,passed_friendId)
        return data == None or int(data.Status) != POSSIBLE_STATUSES.Blocked.value
    
    def check_login_and_token(self, token_in, IP):
        token = JWTHandler.JWTgenerator.ValidateToken(token_in)
        userId = token["Id"]
        code = StatusRequests.FetchLogin(userId, IP)
        if code != 200:
            raise StatusException.WhenUserNotLoggedIn()
        return userId    