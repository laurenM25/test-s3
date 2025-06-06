
# old, not using


from flask import Flask, render_template, request, jsonify
from functions import generate_presigned_url
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-url', methods=['POST'])
def generate_url():
    data = request.get_json()
    if not data or 'file_name' not in data or 'content_type' not in data:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    file_name = data['file_name']
    content_type = data['content_type']

    print(f"Filename: {file_name}. Content type: {content_type}")

    url = generate_presigned_url(file_name, content_type)
    print("generated presigned url:", url)

    print(f"Content type vs upload header --> content type is same as header, which is: {content_type}")

    if url:
        return jsonify({'url': url})
    else:
        return jsonify({'error': 'Failed to generate URL'}), 500

if __name__ == '__main__':
    app.run(debug=True)
