import json


class RedisConfig:
    
    def __init__(self, host, port, db):
        self.host = host
        self.port = port
        self.db = db
        
        
    @staticmethod
    def from_json(json_dict):
        return RedisConfig(json_dict["host"],
                           json_dict["port"],
                           json_dict["db"])
        
    @staticmethod   
    def get_redis_settings():
        configurations = json.load(open("appsettings.json"))
        redis_settings = str(configurations["Redis"]).replace("'",'"')
        data = json.loads(redis_settings, object_hook=RedisConfig.from_json)
        return data