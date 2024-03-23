class Paths:
    def __init__(self, login, fetchStatus, logout):
        self.Login : str = login
        self.FetchStatus: str = fetchStatus
        self.Logout: str = logout
        
    @staticmethod
    def from_json(json_dict):
        return Paths(json_dict["Login"], 
                        json_dict["FetchStatus"],
                        json_dict["Logout"])
    