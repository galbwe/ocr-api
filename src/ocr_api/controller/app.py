from flask import Flask, request
import pytesseract as pt
from PIL import Image


app = Flask(__name__)


@app.route('/ping')
def ping():
    return "PONG"


@app.route('/images', methods=['GET', 'POST'])
def image_collection_controller():
    if request.method == 'POST':
        file = request.files.get('file')
    elif request.method == 'GET':
        


@app.route('/images/<id>', methods=['GET', 'PUT', 'DELETE'])
def image_controller(id):
    pass


@app.route('/images/<id>/convert-to-text', methods=['GET'])
def convert_image_to_text(id):
    img = Image.open(file)
    text = pt.image_to_string(img)
    return text


@app.route('/images/<id>/ocr-results', methods=['GET'])
def get_image_results():
    pass


@app.route('/ocr-results', methods=['GET'])
def ocr_results_collection_controller():
    pass


@app.route('/ocr-results/<id>', methods=['GET', 'DELETE'])
def ocr_results_controller(id):
    pass


@app.route('/convert-image', methods=['POST'])
def add_image():
