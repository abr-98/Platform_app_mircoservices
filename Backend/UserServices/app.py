from Utility_Module.CreateApp import CreateAppInstanceSingleton, CreateAppInstance
from flask_cors import CORS
from UserServices.UserController.UserController import app_file_user
from UserServices.UserController.RegistrationController import app_file_registration

app_creator: CreateAppInstance = CreateAppInstanceSingleton.GetInstance()
app = app_creator.get_app()
db = app_creator.get_db()
CORS(app)
app.app_context().push()
db.create_all()
app.register_blueprint(app_file_user)
app.register_blueprint(app_file_registration)

if __name__ == '__main__':
    app.run(port=5000)