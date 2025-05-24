from flask import Flask, render_template, request, jsonify
from functions import generate_presigned_url
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-url', methods=['POST'])
def generate_url():
    file_name = request.form['file_name']
    content_type = request.form['content_type']

    url = generate_presigned_url(file_name, content_type)
    if url:
        return jsonify({'url': url})
    else:
        return jsonify({'error': 'Failed to generate URL'}), 500

if __name__ == '__main__':
    app.run(debug=True)
