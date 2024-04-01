import json

class AWSConfig:
    def __init__(self, access_key, secret_key, region, bucket_name):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region
        self.bucket_name = bucket_name
    
    @staticmethod
    def from_json(json_dict):
        return AWSConfig(json_dict["AccessKey"],
                         json_dict["SecretKey"],
                         json_dict["Region"],
                         json_dict["Bucket"])
    
    @staticmethod   
    def get_aws_settings():
        configurations = json.load(open("appsettings.json"))
        elastic_settings = str(configurations["AWS"]).replace("'",'"')
        data:AWSConfig = json.loads(elastic_settings, object_hook=AWSConfig.from_json)
        return data
