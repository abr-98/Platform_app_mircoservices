import json

from Utility_Module.CheckLoginStatus.Paths import Paths

class OnineStatusAuth:
    def __init__(self, URL:str, paths: Paths):
        self.Url = URL
        self.Paths = paths
    
    @staticmethod   
    def get_auth_settings():
        configurations = json.load(open("appsettings.json"))
        auth_settings = str(configurations["OnlineStatusAuth"]).replace("'",'"')
        values = json.loads(auth_settings)
        paths: Paths = Paths.from_json(values['Paths'])
        return OnineStatusAuth(values["URL"], paths)
    
