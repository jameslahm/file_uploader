import uuid
from flask import Flask,request,jsonify
from flask.globals import current_app
from flask.helpers import send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SECRET = "jcnabckydusja"
UPLOAD_DIR = os.path.join(BASE_DIR,"static")
API_BASE = "http://139.196.81.14:7998"

@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    token = request.headers.get("Authorization","")

    if token!=SECRET:
        return jsonify({"error":"bad request","success":False}),200

    if 'file' not in request.files:
        return jsonify({"error":"no file", "success": False}),200
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error":"no file", "success":False}),200
    if file :
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)
        filename = secure_filename(file.filename)
        random_string  = uuid.uuid4().hex
        filename = random_string + filename 
        
        file.save(os.path.join(UPLOAD_DIR, filename))
        return jsonify({"url":API_BASE + '/upload/'+filename,"success":True}),200

@app.route('/upload/<filename>',methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR,filename)

if __name__=="__main__":
    app.run("0.0.0.0",port=7998)