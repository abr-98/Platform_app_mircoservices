import datetime as dt
from enum import Enum
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
db: SQLAlchemy = app_creater.get_db()

POSSIBLE_STATUSES = Enum("POSSIBLE_STATUSES", ["NotVerified", "Verified"])

class User(db.Model):
    __tablename__="User"
    
    UserId = db.Column(db.Text, primary_key=True, unique = True)
    Name = db.Column(db.Text, nullable=False)
    Email = db.Column(db.Text, nullable=False)
    Password = db.Column(db.Text)
    PhoneNo = db.Column(db.Text)
    CreateDate = db.Column(db.DateTime)
    Interests = db.Column(db.Text)
    About = db.Column(db.Text)
    Location = db.Column(db.Text)
    ProfilePic = db.Column(db.Text)
    Status = db.Column(db.Text)
    
    def __init__(self, userId, name, email, phoneNo, about, location):
        self.UserId : str = userId
        self.Name : str = name
        self.Email : str = email
        self.Password : bytes= None
        self.PhoneNo: str = phoneNo
        self.CreateDate : dt.datetime = dt.datetime.now()
        self.Interests : str = None
        self.About : str = about
        self.Location : str  = location
        self.ProfilePic : str = None
        self.Status : str = POSSIBLE_STATUSES.NotVerified.value
        
        
    def updateValue(self, field, value: str):
        if field == "Password":
            value_coded = bcrypt.hashpw(str.encode(value),bcrypt.gensalt(12)).decode('utf-8')
        else:
            value_coded = value
        setattr(self, field, value_coded)
        
    def checkPassword(self, password):
        return bcrypt.checkpw(str.encode(password), str.encode(self.Password))
    
    def verifUser(self):
        self.Status = POSSIBLE_STATUSES.Verified.value
        
    def is_authenticated(self):
        return int(self.Status) == POSSIBLE_STATUSES.Verified.value
    
    def is_active(self):
        return True
    
    def get_id(self):
        return self.UserId
    
    def is_anonymous(self):
        return False
        
    @staticmethod
    def from_json(json_dict):
        return User(json_dict['UserId'], 
                        json_dict['Name'],
                        json_dict['Email'],
                        json_dict['PhoneNo'],
                        json_dict['About'],
                        json_dict['Location'])
        

