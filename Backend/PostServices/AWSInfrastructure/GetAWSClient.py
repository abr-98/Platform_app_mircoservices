import boto3

from PostServices.AWSInfrastructure.AWSConfig import AWSConfig

class CreateAWSClient:

    @staticmethod
    def GetClient():
        awsConfig : AWSConfig = AWSConfig.get_aws_settings()
        
        s3client = boto3.client('s3', 
                                aws_access_key_id = awsConfig.access_key,
                                aws_secret_access_key = awsConfig.secret_key,
                                region_name = awsConfig.region)
        

        return s3client, awsConfig.bucket_name
    