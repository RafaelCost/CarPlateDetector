from flask import Flask, render_template, request
from werkzeug import secure_filename
import PlateDetection as plate
import os
from flask_cors import CORS, cross_origin
import pymongo
from pymongo import MongoClient
import base64
from skimage.io import imread

client = MongoClient("mongodb://localhost:27017/CarPlateDetector") # specifying the database port, login, and password
db = client['CarPlateDetector']
plates_collection = db['plates']
plateNumber = ""
imgLocal = ""

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './upload_images/'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/uploader', methods = ['POST'])
def uploader():
   if request.method == 'POST':
      print(request.files)
      if 'file' not in request.files:
         return "ERRO AO ENVIAR A IMAGEM"
      else:
         global plateNumber
         global imgLocal
         f = request.files['file']
         f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))

         p = plate.predict_car_plate(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))
         plateNumber = p
         imgLocal = os.path.join(app.config['UPLOAD_FOLDER'],f.filename)
         print(imgLocal)
         print(p)
         return p

@app.route('/savePlate', methods = ['POST'])
def savePlate():
   if request.method == 'POST':
      print(request.json)
      if 'value' not in request.json:
         return "ERRO AO ENVIAR A IMAGEM"
      else:
         global plateNumber
         global imgLocal
         encoded_string = base64.b64encode(imread(imgLocal))

         new_data = {'image': encoded_string,
                  'local':imgLocal,
                  'plate':plateNumber,
                  'accepted_predict':request.json['value']}

         plates_collection.insert_one(new_data)

         return "Obrigado pela avaliação"

if __name__ == '__main__':
   app.run(debug = True)
