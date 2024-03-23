from GroupServices.Core.GroupException import *
from Utility_Module.CheckLoginStatus.StatusException import UserNotLoggedIn


class ErrorCodeHandler:
    def __init__(self, ex: Exception):
        self.ex = ex
        self.switcher = None
    
    def init_cases(self):
        self.switcher={
            GroupIdAlreadyExists: self.return_error_and_Code(self.ex,405),
            GroupDoesNotExist: self.return_error_and_Code(self.ex, 404),
            UserNotLoggedIn: self.return_error_and_Code(self.ex, 401),
            OnlyGroupAdminAccess: self.return_error_and_Code(self.ex, 401)
        }
    
    def Get_codes_from_exception(self):
        self.init_cases()
        message, code =  self.switcher.get(self.ex.__class__, self.return_run_time_failure(self.ex))
        return message, code

    
    def return_run_time_failure(self,exception):
        return f"Requests Failed with errors {str(exception)}",417
    
    def return_error_and_Code(self,exception, code):
        return f"{str(exception)}",code
    