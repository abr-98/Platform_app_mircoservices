import json

class Postgres:
    def __init__(self, database, host, user, password, port):
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.port = port
    
    @staticmethod
    def from_json(json_dict):
        return Postgres(json_dict["database"], 
                        json_dict["host"],
                        json_dict["user"],
                        json_dict["password"],
                        json_dict["port"])
    
    @staticmethod   
    def get_postgres_settings():
        configurations = json.load(open("appsettings.json"))
        postgres_settings = str(configurations["Postgres"]).replace("'",'"')
        return json.loads(postgres_settings, object_hook=Postgres.from_json)

    
    
    