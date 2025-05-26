#testing in file

import boto3
import logging
from botocore.exceptions import ClientError
import os
import dotenv
import requests
from urllib.parse import urlparse
import re

dotenv.load_dotenv()

aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')

s3 = boto3.client(service_name = 's3', region_name="us-east-1", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
print(aws_access_key_id)

print(repr(aws_access_key_id))
print(repr(aws_secret_access_key))

def upload_file_bucket(file_name,bucket="new-bucket-2341",filepath=None):
    if filepath is None:
        filepath = file_name
    try:
        response = s3.upload_file(file_name,bucket,filepath)
    except ClientError as e:
        logging.error(e)

def ensure_valid_file_name(url, file_name, filepath=None):
    file_name = file_name.replace(" ", "-")
    file_name = re.sub(r'[<>:"/\\|?*]', '', file_name)

    file_extension = os.path.splitext(urlparse(url).path)[1]
    
    if len(file_name.split(".")) == 1:
        file_name += file_extension
    elif len(file_name.split(".")) == 2:
        #check if correct ending
        if file_name.split(".")[1] != file_extension.strip("."):
            file_name = file_name.split(".")[0] + file_extension
    else:
        file_name = file_name.replace(file_extension,"").replace(".","-") + file_extension

    if filepath: #ensure valid filepath leading up to where filename should be stored
        filepath = re.sub(r'[<>:"\\|?*]', '', filepath)
        if filepath[-1] == "/":
            filepath = filepath[:-1]
        filepath = filepath + "/" + file_name

    return file_name,filepath
     

def create_file_and_upload(url,file_name,filepath=None):
    response = requests.get(url)
    file_name, filepath = ensure_valid_file_name(url, file_name, filepath)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        upload_file_bucket(file_name,'new-bucket-2341',filepath)
    else:
        print("did not get valid response from the url, so did not upload")

url = "https://www.johnnyseeds.com/dw/image/v2/BJGJ_PRD/on/demandware.static/-/Sites-jss-master/default/dw7d92704e/images/products/herbs/02390_03_giantofitaly.jpg?sw=800&sh=800"
create_file_and_upload(url,"path/once-more-seed.pdf","test-folder")
