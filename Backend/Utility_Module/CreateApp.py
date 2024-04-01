import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import redis
from Utility_Module.Postgres.DatabaseConnectionSetter import DatabaseConnectionSetter
from Utility_Module.RedisInfrastructure.RedisClient import RedisClient

class CreateAppInstance:
    
    def __init__(self) -> None:
         self.app = None
         self.db = None
         self.redis = None
         self.logger = None
             
    def createApp(self):
        self.app = Flask(__name__)

        self.app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseConnectionSetter.create_database_url()
        self.app.config["SESSION_PERMANENT"] = False
        self.app.config["SESSION_TYPE"] = "filesystem"
        self.app.config['SECRET_KEY'] = "b'_5#y278sajnc\sdb*7sbc'"
        logging.basicConfig(filename="app.log", filemode="w", format='%(asctime)s - %(message)s',datefmt= '%d-%b-%y %H:%M:%S')
        self.db = SQLAlchemy()        
        self.redis = RedisClient.GetClient()
        self.logger = logging.getLogger("Colab-Platform")
        
        self.db.init_app(self.app)

        
    def get_app(self) -> Flask:
        return self.app
    
    def get_db(self) -> SQLAlchemy:
        return self.db
    
    
    def get_Redis(self) -> redis.Redis:
        return self.redis
    
    def get_logger(self) -> logging.Logger:
        return self.logger


class CreateAppInstanceSingleton:
    
    
    app_instance: CreateAppInstance = None
            
    def GetInstance():
        if CreateAppInstanceSingleton.app_instance == None:
            CreateAppInstanceSingleton.app_instance = CreateAppInstance()
            CreateAppInstanceSingleton.app_instance.createApp()
            
        return CreateAppInstanceSingleton.app_instance
            
             