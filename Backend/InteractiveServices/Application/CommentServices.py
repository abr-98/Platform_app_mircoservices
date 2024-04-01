import logging
from InteractiveServices.Core.CommentResult import CommentResult
from InteractiveServices.Core.Comments import Comments
from InteractiveServices.Infrastructure.CommentsDataRepository import CommentDataRepository
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton
from Utility_Module.JWTHandler import JWTHandler
from Utility_Module.CheckLoginStatus.StatusException import StatusException
from Utility_Module.CheckLoginStatus.StatusRequests import StatusRequests


app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
logger : logging.Logger = app_creater.get_logger()

class CommentServices:
    
    def __init__(self):
        self.CommentRepository = CommentDataRepository()
        
    def Comment(self, token_in, IP, postId, comment) -> CommentResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            self.CommentRepository.save(Comments(userId, postId, comment))
            return CommentResult(userId, postId)
        except Exception as e:
            return CommentResult.WhenLikeRecordsOperationsAreFailed(e)

    def FetchComments(self, token_in, IP, postId) -> CommentResult:
        try:
            userId = self.check_login_and_token(token_in, IP)
            likes = self.CommentRepository.fetchAll(postId)
            return CommentResult.WhenLikeRecordsAreFetched(likes)
        except Exception as e:
            return CommentResult.WhenLikeRecordsOperationsAreFailed(e)

    def check_login_and_token(self, token_in, IP):
        token = JWTHandler.JWTgenerator.ValidateToken(token_in)
        userId = token["Id"]
        code = StatusRequests.FetchLogin(userId, IP)
        if code != 200:
            raise StatusException.WhenUserNotLoggedIn()
        return userId    