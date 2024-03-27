from SearchServices.SearchResults import SearchResult
from Utility_Module.Elastic.Infrastructure.EntitiesHandler import EntitiesHandler


class SearchService:
    
    def __init__(self):
        self.ElasticSearchRepo = EntitiesHandler()
        
        
    def search(self, value):
        try:
            data = self.ElasticSearchRepo.search_entity(value)
            return SearchResult.WhenDataIsSearched(data)
        except Exception as e:
            return SearchResult.WhenDataSearchFails(e)