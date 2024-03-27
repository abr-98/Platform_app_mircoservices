from Utility_Module.Elastic.Infrastructure.Entities import Entities


class SearchResult:
    def __init__(self, returnData, Message):
         self.ReturnData = returnData
         self.Message = Message
         
    @staticmethod
    def WhenDataIsSearched(return_data):
        return DataSearched(return_data)
    
    @staticmethod
    def WhenDataSearchFails(ex: Exception):
        return DataSearchFailed(ex)
    
    
class DataSearched(SearchResult):
    
    def __init__(self, return_data: list):
        self.Message = self.constructMessage(return_data)
        super().__init__(return_data, self.Message)
        
    def constructMessage(self, return_data: list):
        message = "Data "
        for data in return_data:
            enitity : Entities = data
            message+=f"{enitity.__dict__};"
        return message
            
            
class DataSearchFailed(SearchResult):
    
    def __init__(self, ex : Exception):
        super().__init__("", "")
        self.Message = f"The request could not be fulfilled {str(ex)}"
        self.ex = ex