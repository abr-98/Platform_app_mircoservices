from flask import Blueprint, jsonify, request, session
from flask_cors import cross_origin

from InteractiveServices.Application.CommentServices import CommentServices
from InteractiveServices.Core.CommentResult import *
from InteractiveServices.Controllers.ErrorCodeHandler import ErrorCodeHandler

app_file_Comment =Blueprint("Comment",__name__)

class CommentController:
    
    commentServices: CommentServices = CommentServices()
    
    @cross_origin
    @app_file_Comment.route("/Comment")
    def HealthCheck():
        return jsonify(message = "Comment Service reached", status = 200)
    

    @cross_origin
    @app_file_Comment.route("/Comment/Record/<PostId>", methods = ['POST'])
    def Comment(PostId):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = CommentController.GetTokenFromHeader(bearer)
        result:CommentResult = CommentController.commentServices.Comment(token, ip, PostId)
        return_state, status = CommentController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_Comment.route("/Comment/Fetch/<PostId>", methods = ['GET'])
    def Fetch(PostId):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = CommentController.GetTokenFromHeader(bearer)
        result:CommentResult = CommentController.commentServices.FetchComments(token, ip, PostId)
        return_state, status = CommentController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    
    
    def Convert_result_to_code(result:CommentResult):
        if result.__class__ == CommentOperationFailed:
            return CommentController.return_error_codes(result)
        else:
            return CommentController.return_success_response(result)
        
        
    def GetTokenFromHeader(bearer:str):
        if bearer is None:
            bearer = "Bearer 123"
        token = bearer.split(' ')[1]
        return token
    
    def return_success_response(result: CommentResult):
        return result.Message,200
    
    def return_error_codes(result: CommentOperationFailed):
        return ErrorCodeHandler(result.ex).Get_codes_from_exception()