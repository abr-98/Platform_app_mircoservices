
import os
from mypy_boto3_s3 import S3Client
from PostServices.AWSInfrastructure.BlobException import BlobException
from Utility_Module.CreateApp import CreateAppInstance, CreateAppInstanceSingleton
from fileinput import *
from app import AWS,AWS_bucket,logger


app_creater : CreateAppInstance= CreateAppInstanceSingleton.GetInstance()

class BlobRepository:
    
    def upload_file(self, userId, postId, fileName : FileInput):
        try: 
            
            if not os.path.exists(fileName.filename):
                logger.warning("File not found")
                raise Exception("File Not Present")
            AWS.upload_file(Bucket = AWS_bucket, Key= f"{userId}/{postId}", Filename=fileName.filename)
            logger.info("file uploaded")
        except Exception as e:
            raise BlobException.WhenBlobOperationFails(e)
        