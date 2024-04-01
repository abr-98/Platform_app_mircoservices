import logging
from GroupServices.SearchEntityProducer import SearchEntityProducer
from Utility_Module.CreateApp import CreateAppInstanceSingleton, CreateAppInstance
from flask_cors import CORS
from GroupServices.GroupController.GroupController import app_file_group

app_creator: CreateAppInstance = CreateAppInstanceSingleton.GetInstance()
app = app_creator.get_app()
db = app_creator.get_db()
CORS(app)
app.app_context().push()
db.create_all()

app.register_blueprint(app_file_group)

if __name__ == '__main__':
    app.run(port=5000)