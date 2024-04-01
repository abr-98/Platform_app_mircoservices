import json
import os
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from fileinput import FileInput, filename
from app import logger

from PostServices.Core.PostResult import *
from PostServices.Application.PostServices import PostServices


app_file_post =Blueprint("Post",__name__)

class PostController:
    
    postServices: PostServices = PostServices()
    
    @cross_origin
    @app_file_post.route("/Post/Health")
    def HealthCheck():
        return jsonify(message = "Search Service reached", status = 200)
    
    @cross_origin
    @app_file_post.route("/Post/Create", methods = ['POST'])
    def create_group():
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = PostController.GetTokenFromHeader(bearer)
        post_data= request.form.to_dict()
        file = request.files['file']
        file.save(file.filename)
        logger.info("file recieved")
        result:PostResult = PostController.postServices.upload_post(file,post_data,token,ip)
        return_state, status = PostController.Convert_result_to_code(result)
        os.remove(file.filename)
        return jsonify(message = return_state, status = status)
    
    def GetTokenFromHeader(bearer:str):
        if bearer is None:
            bearer = "Bearer 123"
        token = bearer.split(' ')[1]
        return token
    
    def Convert_result_to_code(result:PostResult):
        if result.__class__ == PostOperationsFails:
            return PostController.return_error_codes(result)
        else:
            return PostController.return_success_response(result)
        
        
    def return_success_response(result: PostResult):
        return result.Message,200
    
    def return_error_codes(result: PostOperationsFails):
            return str(result.ex), 417
    