from flask import Blueprint, jsonify, request, session
from flask_cors import cross_origin
import json

from GroupServices.Application.GroupService import GroupServices
from GroupServices.GroupController.ErrorCodeHandler import ErrorCodeHandler
from GroupServices.Core.GroupException import *
from GroupServices.Core.Group import Group
from GroupServices.Core.GroupResult import *


app_file_group =Blueprint("Group",__name__)

class GroupController:
    
    groupServices: GroupServices = GroupServices()
    
    @cross_origin
    @app_file_group.route("/Group")
    def HealthCheck():
        return jsonify(message = "Group Service reached", status = 200)
    
    @cross_origin
    @app_file_group.route("/Group/Create", methods = ['POST'])
    def create_group():
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = GroupController.GetTokenFromHeader(bearer)
        group_data = request.json
        result:GroupResult = GroupController.groupServices.Create(group_data, token, ip)
        return_state, status = GroupController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    
    @cross_origin
    @app_file_group.route("/Group/Fetch/<groupId>", methods = ['GET'])
    def fetch_group(groupId):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = GroupController.GetTokenFromHeader(bearer)
        result:GroupResult = GroupController.groupServices.Fetch(groupId, token, ip)
        return_state, status = GroupController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_group.route("/Group/<groupId>/Interests/<interests>", methods = ['PUT'])
    def update_interests(groupId, interests):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = GroupController.GetTokenFromHeader(bearer)
        result:GroupResult = GroupController.groupServices.UpdateInterest(groupId,interests, token, ip)
        return_state, status = GroupController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_group.route("/Group/<groupId>/Delete", methods = ['DELETE'])
    def delete(groupId):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = GroupController.GetTokenFromHeader(bearer)
        result:GroupResult = GroupController.groupServices.Delete(groupId, token, ip)
        return_state, status = GroupController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    def Convert_result_to_code(result:GroupResult):
        if result.__class__ == GroupRequestFailed:
            return GroupController.return_error_codes(result)
        else:
            return GroupController.return_success_response(result)
            
    def GetTokenFromHeader(bearer:str):
        if bearer is None:
            bearer = "Bearer 123"
        token = bearer.split(' ')[1]
        return token
        
    def return_success_response(result: GroupResult):
        return result.Message,200
    
    def return_error_codes(result: GroupRequestFailed):
        return ErrorCodeHandler(result.ex).Get_codes_from_exception()