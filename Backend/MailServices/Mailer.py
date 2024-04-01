import json

class Mailer:
    def __init__(self, email, password):
        self.email = email
        self.password = password
    
    @staticmethod
    def from_json(json_dict):
        return Mailer(json_dict["email"], 
                        json_dict["password"])
    
    @staticmethod   
    def get_mailer_settings():
        configurations = json.load(open("appsettings.json"))
        mailer_settings = str(configurations["Mailer"]).replace("'",'"')
        values: Mailer = json.loads(mailer_settings, object_hook=Mailer.from_json)
        return values.email, values.password

    
    
    