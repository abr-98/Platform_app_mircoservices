class CommentResult:
    
    def __init__(self, UserId, PostId, Message):
        super().__init__()
        self.UserId = UserId
        self.PostId = PostId
        self.Message = Message
    
    @staticmethod
    def WhenCommentRecordIsCreated(userId, postId):
        return CommentRecordCreated(userId, postId)
    
    @staticmethod
    def WhenLikeRecordsAreFetched(likes):
        return CommentRecordFetched(likes)
    
    @staticmethod
    def WhenLikeRecordsOperationsAreFailed(ex):
        return CommentOperationFailed(ex)
        
class CommentRecordCreated(CommentResult):
    
    def __init__(self, UserId, PostId):
        self.message = f"Comment Record created From {UserId} On PostId {PostId}"
        super().__init__(UserId, PostId, self.message)
        
class CommentRecordFetched(CommentResult):
    
    def __init__(self, comment_list):
        self.comment_list = comment_list
        self.message = f"Comments : {comment_list}"
        super().__init__("", "", self.message)
        
        
class CommentOperationFailed(CommentResult):
    
    def __init__(self, ex):
        self.ex = ex
        self.message = f"Interaction Record creation Failed: {str(ex)}"
        super().__init__("", "", self.message)