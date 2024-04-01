import logging
from Utility_Module.CreateApp import CreateAppInstanceSingleton, CreateAppInstance
from flask_cors import CORS
from Status_Maintainance_Services.StatusController.StatusController import app_file_status



app_creator: CreateAppInstance = CreateAppInstanceSingleton.GetInstance()
app = app_creator.get_app()
db = app_creator.get_db()
CORS(app)
app.app_context().push()
db.create_all()
app.register_blueprint(app_file_status)

if __name__ == '__main__':
    app.run(port=5000)