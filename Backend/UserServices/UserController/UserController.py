from flask import request, jsonify, Blueprint
import flask
from flask_cors import cross_origin
from UserServices.Core.UserExceptions import UserException
from UserServices.UserController.ErrorCodeHandler import ErrorCodeHandler
from UserServices.Application.UserService import UserServices
from UserServices.Core.UserResult import UserResult, UserOperationDenied

app_file_user =Blueprint("User",__name__)

class UserController:
    
    userService: UserServices = UserServices()
    
    @cross_origin
    @app_file_user.route("/User")
    def HealthCheck():
        return jsonify(message = "User Service reached", status = 200)
    
    
    @cross_origin
    @app_file_user.route("/User/UpdateField", methods = ['PUT'])
    def update_field():
        ip = request.remote_addr
        field = request.args['field']
        value = request.args['value']
        bearer = request.headers.get('Authorization')
        token = UserController.GetTokenFromHeader(bearer)
        result: UserResult = UserController.userService.Update(field, value, token, ip)
        return_state, status = UserController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_user.route("/User/Fetch", methods = ['GET'])
    def fetch():
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = UserController.GetTokenFromHeader(bearer)
        result: UserResult = UserController.userService.Fetch(token,ip)
        return_state, status = UserController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_user.route("/User/Delete", methods = ['DELETE'])
    def delete():
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = UserController.GetTokenFromHeader(bearer)
        result: UserResult = UserController.userService.Delete(token, ip)
        return_state, status = UserController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_user.route("/User/Logout", methods = ['POST'])
    def logout():
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = UserController.GetTokenFromHeader(bearer)
        result: UserResult = UserController.userService.Logout(token, ip)
        return_state, status = UserController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = 200)  
            
    def Convert_result_to_code(result:UserResult):
        if result.__class__ == UserOperationDenied:
            return UserController.return_error_codes(result)
        else:
            return UserController.return_success_response(result)
        
        
    def GetTokenFromHeader(bearer:str):
        if bearer is None:
            token = "Bearer 123"
        token = bearer.split(' ')[1]
        return token
            
        
    def return_success_response(result: UserResult):
        return result.Message,200

    def return_error_codes(result: UserOperationDenied):
        return ErrorCodeHandler(result.ex).Get_codes_from_exception()

    
        
        
        
            
    