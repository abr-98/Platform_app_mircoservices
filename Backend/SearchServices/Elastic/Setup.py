from elasticsearch import Elasticsearch

from SearchServices.Elastic.Elastic import Elastic


class ElasticDBSetup:
    
    def __init__(self):
        self.dbInstance : Elasticsearch = None
        
    def SetupDB(self):
       self.dbInstance = Elasticsearch(Elastic.get_elastic_settings(),request_timeout=30)
       self.dbInstance = self.__SetUpAllDb__(self.dbInstance)
        
          
    def __AddEntityIndex__(self, elasticDb: Elasticsearch) ->Elasticsearch:
        index_name = "entity"
        mappings = {
            "dynamic": "strict",
            "properties" : {
                "id":{"type": "text", "analyzer": "standard"},
                "name":{"type": "text", "analyzer": "standard"},
                "interest":{"type": "text", "analyzer": "standard"},
                "type":{"type": "text", "analyzer": "standard"}
            }
        }
        if not elasticDb.indices.exists(index=index_name):
            elasticDb.indices.create(index=index_name, ignore=400, mappings=mappings)
        return elasticDb
            
    def __SetUpAllDb__(self, elasticDb: Elasticsearch):
        elasticDb = self.__AddEntityIndex__(elasticDb)
        return elasticDb
    
    def GetInstance(self) -> Elasticsearch:
        return self.dbInstance
    
            
class ElasticDBSetupSingleton:
    
    dbinstance: ElasticDBSetup = None
            
    def GetInstance() -> ElasticDBSetup:
        if ElasticDBSetupSingleton.dbinstance == None:
            ElasticDBSetupSingleton.dbinstance = ElasticDBSetup()
            
        return ElasticDBSetupSingleton.dbinstance
        
        
    