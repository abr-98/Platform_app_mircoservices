from flask import Blueprint, jsonify, request, session
from flask_cors import cross_origin
from ParticipantServices.Application.ParticipantService import ParticipantServices
from ParticipantServices.ParticipantController.ErrorCodeHandler import ErrorCodeHandler
from ParticipantServices.Core.ParticipantResult import ParticipantRequestFailed, ParticipantResult


app_file_participant =Blueprint("Participant",__name__)

class ParticipantController:
    
    participantServices: ParticipantServices = ParticipantServices()
    
    @cross_origin
    @app_file_participant.route("/Participant")
    def HealthCheck():
        return jsonify(message = "Participant Service reached", status = 200)
    
    @cross_origin
    @app_file_participant.route("/Participant/Join/<GroupId>", methods = ['POST'])
    def RequestJoin(GroupId):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = ParticipantController.GetTokenFromHeader(bearer)
        result:ParticipantResult = ParticipantController.participantServices.ParticipantRequestToAdd(token, ip, GroupId)
        return_state, status = ParticipantController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_participant.route("/Participant/Admin/Add/<GroupId>/<UserId>", methods = ['POST'])
    def AdminAdd(GroupId, UserId):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = ParticipantController.GetTokenFromHeader(bearer)
        result:ParticipantResult = ParticipantController.participantServices.AdminRequestToAdd(token, ip, GroupId, UserId)
        return_state, status = ParticipantController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_participant.route("/Participant/Confirm/<GroupId>", methods = ['PUT'])
    def ConfirmRequest(GroupId):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = ParticipantController.GetTokenFromHeader(bearer)
        result:ParticipantResult = ParticipantController.participantServices.Confirm(token, ip, GroupId)
        return_state, status = ParticipantController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_participant.route("/Participant/Admin/Confirm/<GroupId>/<UserId>", methods = ['PUT'])
    def AdminConfirmation(GroupId, UserId):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = ParticipantController.GetTokenFromHeader(bearer)
        result:ParticipantResult = ParticipantController.participantServices.ConfirmByAdmin(token, ip, GroupId, UserId)
        return_state, status = ParticipantController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_participant.route("/Participant/Admin/Block/<GroupId>/<UserId>", methods = ['PUT'])
    def Block(GroupId, UserId):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = ParticipantController.GetTokenFromHeader(bearer)
        result:ParticipantResult = ParticipantController.participantServices.Block(token, ip, GroupId, UserId)
        return_state, status = ParticipantController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_participant.route("/Participant/Admin/Unblock/<GroupId>/<UserId>", methods = ['PUT'])
    def Unblock(GroupId, UserId):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = ParticipantController.GetTokenFromHeader(bearer)
        result:ParticipantResult = ParticipantController.participantServices.Unblock(token, ip, GroupId, UserId)
        return_state, status = ParticipantController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_participant.route("/Participant/Admin/Remove/<GroupId>/<UserId>", methods = ['DELETE'])
    def Remove(GroupId, UserId):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = ParticipantController.GetTokenFromHeader(bearer)
        result:ParticipantResult = ParticipantController.participantServices.Remove(token, ip, GroupId, UserId)
        return_state, status = ParticipantController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_participant.route("/Participant/Leave/<GroupId>/", methods = ['DELETE'])
    def Leave(GroupId):
        ip = request.remote_addr
        bearer = request.headers.get('Authorization')
        token = ParticipantController.GetTokenFromHeader(bearer)
        result:ParticipantResult = ParticipantController.participantServices.Leave(token, ip, GroupId)
        return_state, status = ParticipantController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    
    def Convert_result_to_code(result:ParticipantResult):
        if result.__class__ == ParticipantRequestFailed:
            return ParticipantController.return_error_codes(result)
        else:
            return ParticipantController.return_success_response(result)
            
    def GetTokenFromHeader(bearer:str):
        if bearer is None:
            token = "Bearer 123"
        token = bearer.split(' ')[1]
        return token
        
    def return_success_response(result: ParticipantResult):
        return result.Message,200
    
    def return_error_codes(result: ParticipantRequestFailed):
        return ErrorCodeHandler(result.ex).Get_codes_from_exception()