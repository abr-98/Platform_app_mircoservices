import json


class MQConfig:

    def __init__(self, url):
        self.url = url
    
    @staticmethod
    def from_json(json_dict):
        return MQConfig(json_dict["URL"])
    
    @staticmethod   
    def get_mq_settings():
        configurations = json.load(open("appsettings.json"))
        mq_settings = str(configurations["RabbitMQ"]).replace("'",'"')
        values: MQConfig = json.loads(mq_settings, object_hook=MQConfig.from_json)
        return values.url
