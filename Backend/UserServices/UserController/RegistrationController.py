from flask import request, jsonify, Blueprint
from flask_cors import cross_origin
from UserServices.UserController.ErrorCodeHandler import ErrorCodeHandler
from UserServices.Core.User import User
from UserServices.Application.RegistrationService import RegistrationServices
import json
from UserServices.Core.UserResult import UserResult, UserOperationDenied

app_file_registration =Blueprint("Registration",__name__)

class RegistrationController:
    
    registrationService: RegistrationServices = RegistrationServices()
    
    @cross_origin
    @app_file_registration.route("/User/Registration")
    def HealthCheck():
        return jsonify(message = "User Service reached", status = 200)
        
    @cross_origin
    @app_file_registration.route("/User/Register", methods = ['POST'])
    def register_user():
        user_data = request.json
        data = json.loads(str(user_data).replace("'",'"'), object_hook= User.from_json)
        result:UserResult = RegistrationController.registrationService.Persist(data)
        return_state, status = RegistrationController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_registration.route("/User/<userId>/Verify/<OTP>/SetPass/<Password>", methods = ['POST'])
    def VerifyAndSetPassword(userId, OTP, Password):
        result:UserResult = RegistrationController.registrationService.Verify(userId,OTP,Password)
        return_state, status = RegistrationController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_registration.route("/User/Login", methods = ['POST'])
    def login():
        ip = request.remote_addr
        userId = request.args["UserId"]
        password = request.args["Password"]
        result: UserResult = RegistrationController.registrationService.Login(userId, password, ip)
        return_state, status = RegistrationController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_registration.route("/User/<userEmail>/Recover", methods = ['POST'])
    def recover(userEmail):
        result: UserResult = RegistrationController.registrationService.Recover(userEmail)
        return_state, status = RegistrationController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
            
    
    def Convert_result_to_code(result:UserResult):
        if result.__class__ == UserOperationDenied:
            return RegistrationController.return_error_codes(result)
        else:
            return RegistrationController.return_success_response(result)
            
        
    def return_success_response(result: UserResult):
        return result.Message,200

    def return_error_codes(result: UserOperationDenied):
        return ErrorCodeHandler(result.ex).Get_codes_from_exception()