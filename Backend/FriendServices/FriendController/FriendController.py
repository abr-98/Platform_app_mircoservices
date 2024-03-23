from flask import Blueprint, jsonify, request, session
from flask_cors import cross_origin

from FriendServices.Application.FriendService import FriendService
from FriendServices.FriendController.ErrorCodeHandler import ErrorCodeHandler
from FriendServices.Core.FriendResult import *


app_file_connection =Blueprint("Connection",__name__)

class FriendController:
    
    friendServices: FriendService = FriendService()
    
    @cross_origin
    @app_file_connection.route("/Connection")
    def HealthCheck():
        return jsonify(message = "Connection Service reached", status = 200)
    
    @cross_origin
    @app_file_connection.route("/User/Connect/<connectid>", methods = ['POST'])
    def Connect(connectid):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = FriendController.GetTokenFromHeader(bearer)
        result: FriendResult = FriendController.friendServices.AddFriend(token, ip, connectid)
        return_state, status = FriendController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_connection.route("/User/Confirm/<connectid>", methods = ['PUT'])
    def Confirm(connectid):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = FriendController.GetTokenFromHeader(bearer)
        result: FriendResult = FriendController.friendServices.ConfirmFriend(token, ip, connectid)
        return_state, status = FriendController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    
    @cross_origin
    @app_file_connection.route("/User/Block/<connectid>", methods = ['PUT'])
    def Block(connectid):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = FriendController.GetTokenFromHeader(bearer)
        result: FriendResult = FriendController.friendServices.BlockFriend(token, ip, connectid)
        return_state, status = FriendController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_connection.route("/User/Remove/<connectid>", methods = ['DELETE'])
    def Remove(connectid):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = FriendController.GetTokenFromHeader(bearer)
        result: FriendResult = FriendController.friendServices.RemoveFriend(token, ip, connectid)
        return_state, status = FriendController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_connection.route("/User/Unblock/<connectid>", methods = ['PUT'])
    def Unblock(connectid):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = FriendController.GetTokenFromHeader(bearer)
        result: FriendResult = FriendController.friendServices.UnblockFriend(token, ip, connectid)
        return_state, status = FriendController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    
    def Convert_result_to_code(result:FriendResult):
        if result.__class__ == FriendRequestFailed:
            return FriendController.return_error_codes(result)
        else:
            return FriendController.return_success_response(result)
        
    def GetTokenFromHeader(bearer:str):
        if bearer is None:
            token = "Bearer 123"
        token = bearer.split(' ')[1]
        return token

    def return_success_response(result: FriendResult):
        return result.Message, 200
        
    def return_error_codes(result: FriendRequestFailed):
        return ErrorCodeHandler(result.ex).Get_codes_from_exception()
        
    