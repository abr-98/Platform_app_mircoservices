from ParticipantServices.Core.Participant import Participant

class ParticipantResult:
    
    def __init__(self, GroupId, UserId, Message):
        super().__init__()
        self.Message = Message
        self.GroupId = GroupId
        self.UserId = UserId
        
    @staticmethod
    def WhenParticipantIsCreated(GroupId, UserId):
        return ParticipantCreated(GroupId, UserId)
    
    @staticmethod
    def WhenParticipantIsConfirmed(GroupId, UserId):
        return ParticipantConfirmed(GroupId, UserId)
    
    @staticmethod
    def WhenParticipantIsBlocked(GroupId, UserId):
        return ParticipantBlocked(GroupId, UserId)
    
    @staticmethod
    def WhenParticipantIsUnblocked(GroupId, UserId):
        return ParticipantUnblocked(GroupId, UserId)
    
    @staticmethod
    def WhenParticipantIsRemoved(GroupId, UserId):
        return ParticipantRemoved(GroupId, UserId)
    
    @staticmethod
    def WhenParticipantIsFetched(Participant):
        return ParticipantFetched(Participant)
    
    @staticmethod
    def WhenParticipantRequestFail(ex: Exception):
        return ParticipantRequestFailed(ex)
    

class ParticipantCreated(ParticipantResult):   
    
    def __init__(self, GroupId, UserId):
        self.message = f"Addition of {UserId} to group {GroupId} is initiated"
        super().__init__(GroupId, UserId, self.message)
        
        
class ParticipantFetched(ParticipantResult):   
    
    def __init__(self, participant : Participant):
        self.message = f"Participant details are {participant.__dict__}"
        super().__init__("", "", self.message)

class ParticipantConfirmed(ParticipantResult):   
    
    def __init__(self, GroupId, UserId):
        self.message = f"{UserId} is a participant of the group {GroupId}"
        super().__init__(GroupId, UserId, self.message)
        
class ParticipantBlocked(ParticipantResult):   
    
    def __init__(self, GroupId, UserId):
        self.message = f"{UserId} is blocked from group {GroupId}"
        super().__init__(GroupId, UserId, self.message)
        
class ParticipantUnblocked(ParticipantResult):   
    
    def __init__(self, GroupId, UserId):
        self.message = f"{UserId} is unblocked from group {GroupId}"
        super().__init__(GroupId, UserId, self.message)
        
class ParticipantRemoved(ParticipantResult):   
    
    def __init__(self, GroupId, UserId):
        self.message = f"{UserId} is removed from group {GroupId}"
        super().__init__(GroupId, UserId, self.message)
        
        
class ParticipantRequestFailed(ParticipantResult):
    
    def __init__(self, ex : Exception):
        super().__init__("", "",None)
        self.message = f"The request could not be fulfilled {str(ex)}"
        self.ex = ex