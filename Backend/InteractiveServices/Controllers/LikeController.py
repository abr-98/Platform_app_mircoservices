from flask import Blueprint, jsonify, request, session
from flask_cors import cross_origin

from InteractiveServices.Application.LikeServices import LikeServices
from InteractiveServices.Core.LikeResult import *
from InteractiveServices.Controllers.ErrorCodeHandler import ErrorCodeHandler

app_file_like =Blueprint("Like",__name__)

class LikeController:
    
    likeServices: LikeServices = LikeServices()
    
    @cross_origin
    @app_file_like.route("/Like")
    def HealthCheck():
        return jsonify(message = "Like Service reached", status = 200)
    

    @cross_origin
    @app_file_like.route("/Like/Record/<PostId>", methods = ['POST'])
    def Like(PostId):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = LikeController.GetTokenFromHeader(bearer)
        result:LikeResult = LikeController.likeServices.Like(token, ip, PostId)
        return_state, status = LikeController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_like.route("/Like/Fetch/<PostId>", methods = ['GET'])
    def Fetch(PostId):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = LikeController.GetTokenFromHeader(bearer)
        result:LikeResult = LikeController.likeServices.FetchLikes(token, ip, PostId)
        return_state, status = LikeController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    
    
    def Convert_result_to_code(result:LikeResult):
        if result.__class__ == LikeRecordOperationFailed:
            return LikeController.return_error_codes(result)
        else:
            return LikeController.return_success_response(result)
        
        
    def GetTokenFromHeader(bearer:str):
        if bearer is None:
            bearer = "Bearer 123"
        token = bearer.split(' ')[1]
        return token
    
    def return_success_response(result: LikeResult):
        return result.Message,200
    
    def return_error_codes(result: LikeRecordOperationFailed):
        return ErrorCodeHandler(result.ex).Get_codes_from_exception()