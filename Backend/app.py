from Utility_Module.Elastic.Setup import ElasticDBSetup
from Utility_Module.CreateApp import CreateAppInstanceSingleton, CreateAppInstance
from flask_cors import CORS
from UserServices.UserController.UserController import app_file_user
from UserServices.UserController.RegistrationController import app_file_registration
from Status_Maintainance_Services.StatusController.StatusController import app_file_status
from ParticipantServices.ParticipantController.ParticipantController import app_file_participant
from GroupServices.GroupController.GroupController import app_file_group
from FriendServices.FriendController.FriendController import app_file_connection
from SearchServices.SearchContorller import app_file_search

app_creator: CreateAppInstance = CreateAppInstanceSingleton.GetInstance()
app = app_creator.get_app()
db = app_creator.get_db()
CORS(app)
app.app_context().push()
db.create_all()
elasticDb = app_creator.get_elastic()
elasticdb = ElasticDBSetup.SetUpAllDb(elasticDb)
app.register_blueprint(app_file_user)
app.register_blueprint(app_file_status)
app.register_blueprint(app_file_registration)
app.register_blueprint(app_file_participant)
app.register_blueprint(app_file_group)
app.register_blueprint(app_file_connection)
app.register_blueprint(app_file_search)
if __name__ == '__main__':
    app.run(port=5000)