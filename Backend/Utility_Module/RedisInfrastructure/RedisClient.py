from Utility_Module.RedisInfrastructure.RedisConfig import RedisConfig
import redis

class RedisClient:

    
    @staticmethod
    def GetClient():
        redisConfig : RedisConfig = RedisConfig.get_redis_settings()
        
        redisClient = redis.Redis(host=redisConfig.host, port= int(redisConfig.port), db= int(redisConfig.db),decode_responses=True)
        
        return redisClient