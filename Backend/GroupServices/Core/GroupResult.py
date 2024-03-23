from GroupServices.Core.Group import Group

class GroupResult:
    
    def __init__(self, GroupId, GroupName, Message):
        super().__init__()
        self.Message = Message
        self.GroupId = GroupId
        self.GroupName = GroupName
        
    @staticmethod
    def WhenGroupIsCreated(GroupId, GroupName):
        return GroupCreated(GroupId, GroupName)
    
    @staticmethod
    def WhenGroupIsFetched(Group):
        return GroupFetched(Group)
    
    @staticmethod
    def WhenGroupIsUpdated(GroupId):
        return GroupInterestsUpdated(GroupId)
    
    @staticmethod
    def WhenGroupIsDeleted(GroupId):
        return GroupDeleted(GroupId)
    
    @staticmethod
    def WhenGroupRequirementsFails(ex: Exception):
        return GroupRequestFailed(ex)
        
    
class GroupCreated(GroupResult):
    
    def __init__(self, GroupId, GroupName):
        self.message = f"Group {GroupName} is created with Id {GroupId}"
        super().__init__(GroupId, GroupName, self.message)
        
class GroupFetched(GroupResult):
    
    def __init__(self, Group: Group):
        self.message = f"Group details {Group.__dict__}"
        self.Group = Group
        super().__init__("","", self.message)
        
class GroupRequestFailed(GroupResult):
    
    def __init__(self, ex: Exception):
        super().__init__("", "", None)
        self.message = f"The request could not be fulfilled {str(ex)}"
        self.ex = ex
        
class GroupInterestsUpdated(GroupResult):
    
    def __init__(self, GroupId):
        self.message = f"Interests are updated for group {GroupId}"
        super().__init__(GroupId,"", self.message)
    
class GroupDeleted(GroupResult):
    
    def __init__(self, GroupId):
        self.message = f"Group {GroupId} is deleted"
        super().__init__(GroupId,"", self.message)