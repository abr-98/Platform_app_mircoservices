import logging
from InteractiveServices.Core.LikeResult import LikeResult
from InteractiveServices.Core.Likes import Likes
from InteractiveServices.Infrastructure.LikesDataRepository import LikeDataRepository
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton
from Utility_Module.JWTHandler import JWTHandler
from Utility_Module.CheckLoginStatus.StatusException import StatusException
from Utility_Module.CheckLoginStatus.StatusRequests import StatusRequests


app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
logger : logging.Logger = app_creater.get_logger()

class LikeServices:
    
    def __init__(self):
        self.LikeRepository = LikeDataRepository()
        
    def Like(self, token_in, IP, postId) -> LikeResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            self.LikeRepository.save(Likes(userId, postId))
            return LikeResult.WhenLikeRecordIsCreated(userId, postId)
        except Exception as e:
            return LikeResult.WhenLikeRecordsOperationsAreFailed(e)

    def FetchLikes(self, token_in, IP, postId) -> LikeResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            likes = self.LikeRepository.fetchAll(postId)
            return LikeResult.WhenLikeRecordsAreFetched(likes)
        except Exception as e:
            return LikeResult.WhenLikeRecordsOperationsAreFailed(e)

    def check_login_and_token(self, token_in, IP):
        token = JWTHandler.JWTgenerator.ValidateToken(token_in)
        userId = token["Id"]
        code = StatusRequests.FetchLogin(userId, IP)
        if code != 200:
            raise StatusException.WhenUserNotLoggedIn()
        return userId    