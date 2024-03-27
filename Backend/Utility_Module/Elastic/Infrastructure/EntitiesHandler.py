from elasticsearch import Elasticsearch
from Utility_Module.Elastic.Infrastructure.Entities import Entities
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton
from Utility_Module.Elastic.Infrastructure.EntityException import EntityException
import json

app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()
elasticDb: Elasticsearch = app_creater.get_elastic()
index_name = "entity"

class EntitiesHandler:
        
    def store_entity(self, entity: Entities):
        doc ={
            "id": entity.id,
            "name": entity.name,
            "interest": entity.interests,
            "type": entity.type
        }
        
        elasticDb.index(index=index_name, id=entity.id, document=doc)
        
    def search_entity(self,value):
        query = {
            "bool": {
                "should":{
                    "multi_match":
                        {
                            "query": value,
                            "fields": [
                                "id",
                                "name"
                            ]
                        }
                    }
                }
        } 
        resp = elasticDb.search(index=index_name, query=query)
        if resp.meta.status == 200:
            data = resp['hits']['hits']
            if len(data) == 0:  
                raise EntityException.WhenEntityNotPresent(value)
            else:
                return self.extract_data_from_response(data)
        else: 
            raise EntityException.WhenEntitySearchFailed(Exception("Server error"))
        
            
        
    def delete_entity(self, entity_id):
        elasticDb.delete(index=index_name ,id =entity_id)  
        
    def update_entity_name(self, entity_id, field, value):
        elasticDb.update(index=index_name, id= entity_id, doc= {field:value})     
        
    def extract_data_from_response(self,resp : list):
        return_data ={}
        for data in resp:
            return_data[float(data["_score"])] = json.loads(str(data["_source"]).replace("'",'"'), object_hook=Entities.from_json)
            
        return_data_sorted = dict(sorted(return_data.items()))
        return list(return_data_sorted.values())
            
        
           