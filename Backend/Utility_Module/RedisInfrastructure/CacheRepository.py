from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton
import redis
import time

from Utility_Module.RedisInfrastructure.CacheException import CatchException

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
redisClient: redis.Redis = app_creater.get_Redis()

class CacheRepository:

    def store(self, id, value):
        try:
            redisClient.set(id, value, ex = 43200)
        except Exception as e:
            raise CatchException.WhenCacheOperationFails(e)
        
    def fetch(self, id):
        try:
            data = redisClient.get(id)
            if data == None:
                return None
            else:
                return data
        except Exception as e:
            raise CatchException.WhenCacheOperationFails(e)