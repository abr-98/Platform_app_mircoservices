import json
import pika
import logging

from SearchServices.Elastic.Infrastructure.Entities import Entities
from SearchServices.Elastic.Infrastructure.EntitiesHandler import EntitiesHandler
from SearchServices.MQConfig import MQConfig

class AddEntityConsumer:
    
    def __init__(self, logging :logging.Logger):
        self.url = MQConfig.get_mq_settings()
        self.elasticEntityHandler = EntitiesHandler()
        self.logging  = logging
        
    def setup(self):
        params = pika.URLParameters(self.url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        
        channel.queue_declare(queue="elastic", durable = True)
        self.logging.info("Elastic entity consumer setup")
        
        channel.basic_consume(queue="elastic", on_message_callback=self.callback, auto_ack=True)
        
        channel.start_consuming()
        
    def callback(self,ch, method, properties, body):
        
        self.logging.info("Recived in elastic entity consumer")
        
        if properties.content_type == "add_requested":
            data= json.loads(body, object_hook=Entities.from_json)
            self.elasticEntityHandler.store_entity(data)
            self.logging.info("Entity Added")
            
        elif properties.content_type == "delete_requested":
            data : Entities = json.loads(body, object_hook=Entities.from_json)
            self.elasticEntityHandler.delete_entity(data.id)
            self.logging.info("Entity Removed")
        
class AddEntityConsumerFactory:
    
    consumer_instance: AddEntityConsumer = None
            
    def GetInstance(logger : logging.Logger) -> AddEntityConsumer:
        if AddEntityConsumerFactory.consumer_instance == None:
            AddEntityConsumerFactory.consumer_instance = AddEntityConsumer(logger)
            
        return AddEntityConsumerFactory.consumer_instance
    