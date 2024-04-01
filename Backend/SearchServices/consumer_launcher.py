from flask_cors import CORS
from SearchServices.AddEntityConsumer import AddEntityConsumer, AddEntityConsumerFactory
from SearchServices.Elastic.Elastic import Elastic
from SearchServices.Elastic.Setup import ElasticDBSetup, ElasticDBSetupSingleton
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton
import logging

from SearchServices.SearchContorller import app_file_search


app_creator: CreateAppInstance = CreateAppInstanceSingleton.GetInstance()
app = app_creator.get_app()
db = app_creator.get_db()
CORS(app)
app.app_context().push()
db.create_all()
elasticDb = ElasticDBSetupSingleton.GetInstance()
elasticDb.SetupDB()
app.register_blueprint(app_file_search)


if __name__ == '__main__':
    logger = app_creator.get_logger()
    mq = AddEntityConsumer(logger)
    mq.setup()