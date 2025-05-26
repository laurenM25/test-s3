from flask import Flask, render_template, request, jsonify
import os
import boto3
import logging
from botocore.exceptions import ClientError
import os
import dotenv
import requests
from urllib.parse import urlparse
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)
dotenv.load_dotenv()

aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')

s3 = boto3.client(service_name = 's3', region_name="us-east-1", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
print(aws_access_key_id)

def upload_file_bucket(file_name,bucket="new-bucket-2341",filepath=None):
    if filepath is None:
        filepath = file_name
    try:
        response = s3.upload_file(file_name,bucket,filepath)
    except ClientError as e:
        logging.error(e)
        print("error uploading")
        return jsonify({'error': 'error uploading'})
    print("successful uploading")
    return jsonify({'success': 'successfully uploaded'})

def ensure_valid_file_name(file_name, url=None, file_ext=None, filepath=None):
    file_name = file_name.replace(" ", "-")
    file_name = re.sub(r'[<>:"/\\|?*]', '', file_name)

    if url:
        file_extension = os.path.splitext(urlparse(url).path)[1]
    if file_ext:
        file_extension = "." + file_ext
    
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

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/url-upload', methods=['POST'])
def create_file_and_upload():
    print("entering function at line 62")
    url = request.form.get("img_url")
    file_name = request.form.get("filename")
    filepath = request.form.get("pathname")

    print("url from user input:", url)
    response = requests.get(url)
    file_name, filepath = ensure_valid_file_name(file_name, url=url, filepath=filepath)
    if response.status_code == 200:
        with open(file_name, 'wb') as file:
            file.write(response.content)
        return upload_file_bucket(file_name,'new-bucket-2341',filepath)

    else:
        print("did not get valid response from the url, so did not upload")
        return jsonify({'error': 'invalid response from url'})
     
@app.route('/file-upload', methods=['POST'])
def save_file_and_upload():
    print("entering function at line 81 (file upload)")
    if 'file' not in request.files:
        return 'No file part in the request', 400

    user_file = request.files['file']
    file_name = request.form.get("filename")
    file_path = request.form.get("pathname")

    # Secure the filename
    if user_file:
        ext = user_file.filename.rsplit('.', 1)[1].lower()
        file_name, file_path = ensure_valid_file_name(file_name,file_ext=ext,filepath=file_path) 
        # Save file locally
        user_file.save(file_name)

        #upload to aws
        return upload_file_bucket(file_name,'new-bucket-2341',file_path)


if __name__ == '__main__':
    app.run(debug=True)
