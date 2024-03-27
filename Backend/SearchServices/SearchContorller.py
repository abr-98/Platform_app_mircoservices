from flask import Blueprint, jsonify
from flask_cors import cross_origin

from SearchServices.SearchResults import *
from SearchServices.SearchService import SearchService
from Utility_Module.Elastic.Infrastructure.EntityException import *


app_file_search =Blueprint("Search",__name__)

class SearchController:
    
    searchServices: SearchService = SearchService()
    
    @cross_origin
    @app_file_search.route("/Search/Health")
    def HealthCheck():
        return jsonify(message = "Search Service reached", status = 200)
    
    @cross_origin
    @app_file_search.route("/Search/<value>", methods = ['POST'])
    def create_group(value):
        result:SearchResult = SearchController.searchServices.search(value)
        return_state, status = SearchController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    def Convert_result_to_code(result:SearchResult):
        if result.__class__ == DataSearchFailed:
            return SearchController.return_error_codes(result)
        else:
            return SearchController.return_success_response(result)
        
        
    def return_success_response(result: SearchResult):
        return result.Message,200
    
    def return_error_codes(result: DataSearchFailed):
        if result.ex.__class__ == EntityNotPresent:
            return str(result.ex), 404
        else:
            return str(result.ex), 417
    