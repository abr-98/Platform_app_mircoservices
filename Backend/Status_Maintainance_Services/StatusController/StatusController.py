from flask import Blueprint, jsonify
from flask_cors import cross_origin
from Status_Maintainance_Services.Application.StatusServices import StatusServices
from Status_Maintainance_Services.Core.Status import Status
from Status_Maintainance_Services.Core.StatusResult import StatusResult, StatusOperationDenied
from Status_Maintainance_Services.Core.OnlineStatusException import LoginDoesNotExist

app_file_status = Blueprint("OnlineStatus",__name__)

class StatusController:
    
    statusService: StatusServices = StatusServices()
    
    @cross_origin
    @app_file_status.route("/Status")
    def HealthCheck():
        return jsonify(message = "Status Service reached", status = 200)
    
    @cross_origin
    @app_file_status.route("/Status/Login/<UserId>/<IP>", methods =['POST'])
    def StatusLogin(UserId,IP):
        result: StatusResult = StatusController.statusService.CreateLogin(Status(UserId, IP))
        return_state, status = StatusController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_status.route("/Status/Fetch/<UserId>/<IP>", methods =['GET'])
    def FetchLogin(UserId,IP):
        result: StatusResult = StatusController.statusService.FetchLogin(UserId, IP)
        return_state, status = StatusController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    @cross_origin
    @app_file_status.route("/Status/Logout/<UserId>/<IP>", methods =['DELETE'])
    def StatusLogout(UserId,IP):
        result: StatusResult = StatusController.statusService.Logout(UserId, IP)
        return_state, status = StatusController.Convert_result_to_code(result)
        return jsonify(message = return_state, status = status)
    
    
    def Convert_result_to_code(result:StatusResult):
        if result.__class__ == StatusOperationDenied:
            return StatusController.return_error_codes(result)
        else:
            return StatusController.return_success_response(result)
        
    def return_success_response(result: StatusResult):
        return result.Message,200

    def return_error_codes(result: StatusOperationDenied):
        if result.ex.__class__ == LoginDoesNotExist:
            return f"{str(result.ex)}", 404
        else:
            return f"{str(result.ex)}", 417
        
        
    
    