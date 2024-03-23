import json
from Utility_Module.CheckLoginStatus.OnlineStatusAuth import OnineStatusAuth
import requests


class StatusRequests:
    
    PathSettings : OnineStatusAuth = OnineStatusAuth.get_auth_settings()
        
    @staticmethod
    def CreateLogin(UserId: str, IP: str):
        path = StatusRequests.PathSettings.Paths.Login.replace("<UserId>",UserId).replace("<IP>",IP)
        url = StatusRequests.PathSettings.Url + path
        results = requests.post(url)
        code = results.status_code
        if (code ==200):
            code =StatusRequests.ExtractStatusFromReturn(results.text)
        return code
    
    @staticmethod
    def FetchLogin(UserId: str, IP: str):
        path = StatusRequests.PathSettings.Paths.FetchStatus.replace("<UserId>",UserId).replace("<IP>",IP)
        url = StatusRequests.PathSettings.Url + path
        results = requests.get(url)
        code = results.status_code
        if (code ==200):
            code =StatusRequests.ExtractStatusFromReturn(results.text)
        return code
    
    @staticmethod
    def Delete(UserId: str, IP: str):
        path = StatusRequests.PathSettings.Paths.Logout.replace("<UserId>",UserId).replace("<IP>",IP)
        url = StatusRequests.PathSettings.Url + path
        results = requests.delete(url)
        code = results.status_code
        if (code ==200):
            code =StatusRequests.ExtractStatusFromReturn(results.text)
        return code
    
    @staticmethod
    def ExtractStatusFromReturn(response: str):
        ret = json.loads(response)
        return int(ret["status"])