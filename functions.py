import boto3
from botocore.exceptions import ClientError
import config
import logging
import time
import hmac
import hashlib
import base64
import urllib.parse

boto3.set_stream_logger('botocore', level=logging.DEBUG) 

def generate_presigned_url(file_name, content_type):
    access_key = config.AWS_ACCESS_KEY_ID
    secret_key = config.AWS_SECRET_ACCESS_KEY
    bucket_name = config.S3_BUCKET

    method = "PUT"
    content_md5 = ""
    expires = int(time.time()) + 3600  # expires in 1 hour
    canonical_resource = f"/{bucket_name}/{file_name}"

    # Construct StringToSign
    string_to_sign = f"{method}\n{content_md5}\n{content_type}\n{expires}\n{canonical_resource}"
    print(f"StringToSign manually constructed:\n>>>{string_to_sign}<<<")

    # Compute Signature
    signature = base64.b64encode(
        hmac.new(secret_key.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha1).digest()
    ).decode('utf-8')

    print("Computed Signature:", signature)

    # URL encode the signature for safe transport in query string
    signature_encoded = urllib.parse.quote(signature)

    # Construct the full presigned URL manually
    presigned_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}" \
                    f"?AWSAccessKeyId={access_key}&Expires={expires}&Signature={signature_encoded}"

    print("Presigned URL:", presigned_url)

    return presigned_url
    

    """
    session = boto3.session.Session(
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
        region_name=config.AWS_REGION
    )
    method = "PUT"
    content_md5 = ""  # usually empty for PUT presigned URLs
    expires = int(time.time()) + 3600  # same value as ExpiresIn when URL generated
    canonical_resource = f"/{config.S3_BUCKET}/{file_name}"

    #printing out to check any mismatch
    string_to_sign = f"{method}\n{content_md5}\n{content_type}\n{expires}\n{canonical_resource}"

    print("StringToSign manually constructed:\n", string_to_sign)

    secret_key = config.AWS_SECRET_ACCESS_KEY.encode('utf-8')
    string_to_sign_bytes = string_to_sign.encode('utf-8')

    signature = base64.b64encode(
        hmac.new(secret_key, string_to_sign_bytes, hashlib.sha1).digest()
    ).decode('utf-8')

    print("Computed signature:", signature)

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
    """