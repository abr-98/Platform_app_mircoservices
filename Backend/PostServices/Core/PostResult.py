from PostServices.Core.Post import Post


class PostResult():
    
    def __init__(self, UserId, Message):
        super().__init__()
        self.UserId = UserId
        self.Message = Message
        
    @staticmethod
    def WhenPostSucceeds(UserId):
        return PostSucceeded(UserId)
    
    @staticmethod
    def WhenPostIsFetched(Post):
        return PostFetched(Post)
    
    @staticmethod
    def WhenPostIsDeleted(UserId):
        return PostDeleted(UserId)
    
    @staticmethod
    def WhenPostOperationsFails(ex):
        return PostOperationsFails(ex)
        
    
class PostSucceeded(PostResult):
    
    def __init__(self, UserId):
        self.message = f"Post is uploaded for {UserId}"
        super().__init__(UserId, self.message)
        
class PostFetched(PostResult):
    
    def __init__(self, post: Post):
        self.message = f"Details: {post.__dict__} "
        super().__init__(post.UserId, self.message)
        
class PostDeleted(PostResult):
    
    def __init__(self, UserId):
        self.message = f"Post is deleted for {UserId}"
        super().__init__(UserId, self.message)
        
class PostOperationsFails(PostResult):
    
    def __init__(self, ex):
        self.ex = ex
        self.message = f"Post Operations fails {str(ex)}"
        super().__init__(None, self.message)

    
        
    