import boto3
from botocore.exceptions import ClientError
import config

def generate_presigned_url(file_name, content_type):
    session = boto3.session.Session(
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_REGION
    )

    s3_client = session.client('s3')

    credentials = session.get_credentials()

    try:
        response = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': config.S3_BUCKET,
                'Key': file_name,
                'ContentType': content_type
            },
            ExpiresIn=3600
        )
        return response
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return None
