import jwt
import datetime as dt

from Utility_Module.JWTHandler.JWTExceptions import JWTExceptions

secret = "my_application_secret"

class JWTgenerator:
    
    @staticmethod
    def generateToken(userId: str, userName: str):
        
        header = {
            "alg":"HS256",
            "typ":"JWT"
        }
        
        payload = {
            "Id": userId,
            "Name": userName,
            "exp": dt.datetime.now() + dt.timedelta(days=1)
        }
        
        encoded_token = jwt.encode(headers = header, payload=payload, key=secret)
        
        return encoded_token
        
    @staticmethod
    def ValidateToken(Token: str):
        try:
            decoded_token = jwt.decode(Token,secret,algorithms=['HS256'], verify=True, options={"verify_signature": True})
            return decoded_token
        except Exception as e:
            raise JWTExceptions.WhenTokenValidationFails(e)
        
