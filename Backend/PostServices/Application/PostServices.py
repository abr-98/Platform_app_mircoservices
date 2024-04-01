import json
import logging
from PostServices.Core.Post import Post
from PostServices.Core.PostResult import PostResult
from PostServices.Infrastructure.PostRepository import PostRepository
from PostServices.AWSInfrastructure.BlobRepository import BlobRepository
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton
from Utility_Module.JWTHandler import JWTHandler
from Utility_Module.CheckLoginStatus.StatusRequests import StatusRequests
from Utility_Module.CheckLoginStatus.StatusException import StatusException
from Utility_Module.RedisInfrastructure.CacheRepository import CacheRepository

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
logger : logging.Logger = app_creater.get_logger()

class PostServices:
    
    def __init__(self):
        self.PostRepository = PostRepository()
        self.BlobRepository = BlobRepository()
        self.CacheRepository = CacheRepository()
        
    def upload_post(self, fileName, post_data, token_in, IP):
        
        try:
            userId = self.check_login_and_token(token_in, IP)
            post_data["UserId"] = userId
            logger.info(f"User {userId} is logged in")
            data = json.loads(str(post_data).replace("'",'"'), object_hook= Post.from_json)
            self.BlobRepository.upload_file(data.UserId, data.PostId, fileName)
            self.PostRepository.save(data)
            logger.info(f"File is uploaded and post is saved")
            return PostResult.WhenPostSucceeds(data.UserId)
        except Exception as e:
            return PostResult.WhenPostOperationsFails(e)
        
        
    def check_login_and_token(self, token_in, IP):
        token = JWTHandler.JWTgenerator.ValidateToken(token_in)
        userId = token["Id"] 
        code = StatusRequests.FetchLogin(userId, IP)
        if code != 200:
            raise StatusException.WhenUserNotLoggedIn()
        return userId   
            
            