import json
import pika
import logging

from MailServices.MQConfig import MQConfig
from MailServices.Mail import Mail
from MailServices.MailerServices import MailServiceInfraSingleton

class MailEventConsumer:
    
    mailer = MailServiceInfraSingleton.GetInstance()
    
    def __init__(self, logging :logging.Logger):
        self.url = MQConfig.get_mq_settings()
        self.logging  = logging
        
    def setup(self):
        params = pika.URLParameters(self.url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        
        channel.queue_declare(queue="mail")
        self.logging.info("mail setup")
        
        channel.basic_consume(queue="mail", on_message_callback=self.callback, auto_ack=True)
        
        channel.start_consuming()
        
    def callback(self, ch, method, properties, body):
        
        self.logging.info("Recived in mail consumer")
        data: Mail = json.loads(body, object_hook=Mail.from_json)
        
        if properties.content_type == "mail_requested":
            MailEventConsumer.mailer.SendMail(data.recieversEmail, data.message, data.subject)
            self.logging.info("Mail sent")
            
    