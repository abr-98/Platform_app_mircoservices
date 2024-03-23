class ParticipantException(Exception):
    
    def __init__(self, message: str,ex: Exception):
        self.message : str = message
        self.ex = ex
        
    def __str__(self) -> str:
        return self.message
    
    @staticmethod
    def WhenParticipantCreationFailed(ex: Exception):
        return ParticipantCreationFailed(ex)
    
    @staticmethod
    def WhenPartcipantFetchFailed(ex: Exception):
        return ParticipantFetchFailed(ex)
    
    @staticmethod
    def WhenParticipantAlreadyExists(groupId, userId):
        return ParticipantAlreadyExists(groupId, userId)
    
    @staticmethod
    def WhenParticipantIsBlocked(groupId, userId):
        return ParticipantIsBlocked(groupId, userId)
    
    @staticmethod
    def WhenParticipantDoesNotExist(groupId, userId):
        return ParticipantDoesNotExist(groupId, userId)
        
    @staticmethod
    def WhenParticipantUpdateFailed(ex: Exception):
        return ParticipantDoesNotExist(ex)
    
    @staticmethod
    def WhenParticipantDeleteFailed(ex: Exception):
        return ParticipantDeleteFailed(ex)
    
class ParticipantCreationFailed(ParticipantException):
    
     def __init__(self, ex: Exception):
        self.message = f"Participant Creation failed: {str(ex)}"
        super().__init__(self.message,ex)
        
class ParticipantFetchFailed(ParticipantException):
    
     def __init__(self, ex: Exception):
        self.message = f"Participant Fetch failed: {str(ex)}"
        super().__init__(self.message,ex)
        
class ParticipantUpdateFailed(ParticipantException):
    
     def __init__(self, ex: Exception):
        self.message = f"Participant update failed: {str(ex)}"
        super().__init__(self.message,ex)
        
class ParticipantDeleteFailed(ParticipantException):
    
     def __init__(self, ex: Exception):
        self.message = f"Participant deletion failed: {str(ex)}"
        super().__init__(self.message,ex)
              
class ParticipantAlreadyExists(ParticipantException):
    
     def __init__(self, groupId, userId):
        self.message = f"User {userId} already exists in {groupId}"
        super().__init__(self.message,None)
        
class ParticipantIsBlocked(ParticipantException):
    
     def __init__(self, groupId, userId):
        self.message = f"User {userId} is blocked from joining {groupId}"
        super().__init__(self.message,None)
        
class ParticipantDoesNotExist(ParticipantException):
    
     def __init__(self, groupId, userId):
        self.message = f"{userId} is not part of this group {groupId}"
        super().__init__(self.message,None)