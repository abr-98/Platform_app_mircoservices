from InteractiveServices.Core.Likes import Likes


class LikeResult:
    
    def __init__(self, UserId, PostId, Message):
        super().__init__()
        self.UserId = UserId
        self.PostId = PostId
        self.Message = Message
        
    @staticmethod
    def WhenLikeRecordIsCreated(userId, postId):
        return LikeRecordCreated(userId, postId)
    
    @staticmethod
    def WhenLikeRecordsAreFetched(likes):
        return LikeRecordFetched(likes)
    
    @staticmethod
    def WhenLikeRecordsOperationsAreFailed(ex):
        return LikeRecordOperationFailed(ex)
        
class LikeRecordCreated(LikeResult):
    
    def __init__(self, UserId, PostId):
        self.message = f"Like Record created From {UserId} On PostId {PostId}"
        super().__init__(UserId, PostId, self.message)
        
class LikeRecordFetched(LikeResult):
    
    def __init__(self, like_list):
        self.list = like_list
        self.message = f"Likes : {like_list}"
        super().__init__("", "", self.message)
        
        
class LikeRecordOperationFailed(LikeResult):
    
    def __init__(self, ex):
        self.ex = ex
        self.message = f"Like Record operation Failed: {str(ex)}"
        super().__init__("", "", self.message)