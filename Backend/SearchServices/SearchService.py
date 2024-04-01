import logging
from SearchServices.AddEntityConsumer import AddEntityConsumer
from SearchServices.SearchResults import SearchResult
from SearchServices.Elastic.Infrastructure.EntitiesHandler import EntitiesHandler
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton
from Utility_Module.JWTHandler import JWTHandler
from Utility_Module.CheckLoginStatus.StatusRequests import StatusRequests
from Utility_Module.CheckLoginStatus.StatusException import StatusException
from Utility_Module.RedisInfrastructure.CacheRepository import CacheRepository

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
logger : logging.Logger = app_creater.get_logger()

class SearchService:
    
    def __init__(self):
        self.ElasticSearchRepo = EntitiesHandler()
        self.CacheHandler = CacheRepository()
        
    def search(self, value, token_in, IP):
        try:
            userId = self.check_login_and_token(token_in, IP)
            logger.info(f"User {userId} logged in")
            data = self.CacheHandler.fetch(value)
            if(data == None):
                data = self.ElasticSearchRepo.search_entity(value)
                self.CacheHandler.store(value, data)
            logger.info(f"data fetched")
            return SearchResult.WhenDataIsSearched(data)
        except Exception as e:
            return SearchResult.WhenDataSearchFails(e)
        
    def check_login_and_token(self, token_in, IP):
        token = JWTHandler.JWTgenerator.ValidateToken(token_in)
        userId = token["Id"]
        code = StatusRequests.FetchLogin(userId, IP)
        if code != 200:
            raise StatusException.WhenUserNotLoggedIn()
        return userId  