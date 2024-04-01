from elasticsearch import Elasticsearch
from flask_cors import CORS
from PostServices.AWSInfrastructure.GetAWSClient import CreateAWSClient
from SearchServices.AddEntityConsumer import AddEntityConsumer
from SearchServices.Elastic.Elastic import Elastic
from SearchServices.Elastic.Setup import ElasticDBSetup
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton
import logging

from PostServices.PostController.PostController import app_file_post


app_creator: CreateAppInstance = CreateAppInstanceSingleton.GetInstance()
app = app_creator.get_app()
db = app_creator.get_db()
CORS(app)
app.app_context().push()
db.create_all()
AWS, AWS_bucket = CreateAWSClient.GetClient()

app.register_blueprint(app_file_post)


if __name__ == '__main__':
    app.run(port=5000)


