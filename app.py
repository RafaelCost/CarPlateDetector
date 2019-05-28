from flask import Flask, render_template, request
from werkzeug import secure_filename
import PlateDetection as plate
import os
from flask_cors import CORS, cross_origin
import pymongo
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/CarPlateDetector") # specifying the database port, login, and password
db = client['Admin']
plates_collection = db['plates']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './upload_images/'

app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/uploader', methods = ['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def uploader():
   if request.method == 'POST':
      if 'file' not in request.files:
         return "ERRO AO ENVIAR A IMAGEM"
      else:
         f = request.files['file']
         f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))

         p = plate.predict_car_plate(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))

         return p



@app.route('/savePlate', methods = ['POST'])
def savePlate():
   if request.method == 'POST':
      if 'image' not in request.files or 'plate'  not in request.files or 'aprovate'  not in request.files:
         return "ERRO OS DADOS"
      else:
         new_data = {'image': request.files['image'],
                  'plate':request.files['image'],
                  'accepted_predict':request.files['image']}

         plates_collection.insert_one(new_data)

         return "Obrigado pela avaliação"


if __name__ == '__main__':
   app.run(debug = True)
