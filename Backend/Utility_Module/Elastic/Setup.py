from elasticsearch import Elasticsearch

from Utility_Module.Elastic.Elastic import Elastic


class ElasticDBSetup:
       
    @staticmethod    
    def AddEntityIndex(elasticDb: Elasticsearch) ->Elasticsearch:
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
            
    @staticmethod
    def SetUpAllDb(elasticDb: Elasticsearch):
        elasticDb = ElasticDBSetup.AddEntityIndex(elasticDb)
        return elasticDb
        

            
        
        
    