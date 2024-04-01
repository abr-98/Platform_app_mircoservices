import json

class Elastic:
    def __init__(self, URL):
        self.URL = URL
    
    @staticmethod
    def from_json(json_dict):
        return Elastic(json_dict["URL"])
    
    @staticmethod   
    def get_elastic_settings():
        configurations = json.load(open("appsettings.json"))
        elastic_settings = str(configurations["Elastic"]).replace("'",'"')
        data:Elastic = json.loads(elastic_settings, object_hook=Elastic.from_json)
        return data.URL
