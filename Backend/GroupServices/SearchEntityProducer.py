import json
import logging
import pika

from GroupServices.MQConfig import MQConfig

class SearchEntityProducer:
    
    def __init__(self, logging :logging.Logger):
        self.url = MQConfig.get_mq_settings()
        self.logging  = logging
        self.channel = None
        
    def setup(self):
        params = pika.URLParameters(self.url)
        connection = pika.BlockingConnection(params)
        self.channel = connection.channel()
        
    def publish(self,method, body):
        properties = pika.BasicProperties(method)
        self.channel.basic_publish(exchange="", routing_key="elastic", body=json.dumps(body.__dict__), properties=properties)