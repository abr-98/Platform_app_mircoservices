from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from Utility_Module.Postgres.DatabaseConnectionSetter import DatabaseConnectionSetter

class CreateAppInstance:
    
    def __init__(self) -> None:
         self.app = None
         self.db = None
             
    def createApp(self):
        self.app = Flask(__name__)

        self.app.config['SQLALCHEMY_DATABASE_URI'] = DatabaseConnectionSetter.create_database_url()
        self.app.config["SESSION_PERMANENT"] = False
        self.app.config["SESSION_TYPE"] = "filesystem"
        self.app.config['SECRET_KEY'] = "b'_5#y278sajnc\sdb*7sbc'"
        self.db = SQLAlchemy()
        self.db.init_app(self.app)

        
        
    def get_app(self) -> Flask:
        return self.app
    
    def get_db(self) -> SQLAlchemy:
        return self.db


class CreateAppInstanceSingleton:
    
    app_instance: CreateAppInstance = None
            
    def GetInstance():
        if CreateAppInstanceSingleton.app_instance == None:
            CreateAppInstanceSingleton.app_instance = CreateAppInstance()
            CreateAppInstanceSingleton.app_instance.createApp()
            
        return CreateAppInstanceSingleton.app_instance
            
             