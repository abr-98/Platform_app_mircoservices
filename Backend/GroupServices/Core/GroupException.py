class GroupException(Exception):
    
    def __init__(self, message: str, ex: Exception):
        self.message : str = message
        self.ex = ex
        
    def __str__(self) -> str:
        return self.message
    
    @staticmethod
    def WhenGroupCreationFails(ex : Exception):
        return GroupCreationFailed(ex)
    
    @staticmethod
    def WhenGroupAlreadyExists(groupId):
        return GroupIdAlreadyExists(groupId)
    
    @staticmethod
    def WhenGroupDoesNotExist(groupId):
        return GroupDoesNotExist(groupId)
    
    @staticmethod
    def WhenGroupFetchFails(ex : Exception):
        return GroupFetchFailed(ex)
    
    @staticmethod
    def WhenGroupUpdationFailed(ex : Exception):
        return GroupUpdationFailed(ex)
    
    @staticmethod
    def WhenGroupDeleteFailed(ex : Exception):
        return GroupDeleteFailed(ex)
    
    @staticmethod
    def NonGroupAdminsMakeChanges(ex : Exception):
        return OnlyGroupAdminAccess(ex)
    
class GroupCreationFailed(GroupException):
    
     def __init__(self, ex: Exception):
        self.message = f"Group Creation failed: {str(ex)}"
        super().__init__(self.message,ex)
        
class GroupIdAlreadyExists(GroupException):
    
     def __init__(self, GroupId):
        self.message = f"Group Already Exists: {GroupId}"
        super().__init__(self.message,None)
        
class OnlyGroupAdminAccess(GroupException):
    
     def __init__(self, GroupId):
        self.message = f"Only group admins can make this change"
        super().__init__(self.message,None)
        
class GroupDoesNotExist(GroupException):
    
     def __init__(self, GroupId):
        self.message = f"Group does not Exist: {GroupId}"
        super().__init__(self.message,None)
        
class GroupFetchFailed(GroupException):
    
     def __init__(self, ex: Exception):
        self.message = f"Group Fetch failed: {str(ex)}"
        super().__init__(self.message,ex)
        
class GroupUpdationFailed(GroupException):
    
     def __init__(self, ex: Exception):
        self.message = f"Group updation failed: {str(ex)}"
        super().__init__(self.message,ex)
        
class GroupDeleteFailed(GroupException):
    
     def __init__(self, ex: Exception):
        self.message = f"Group delete failed: {str(ex)}"
        super().__init__(self.message,ex)