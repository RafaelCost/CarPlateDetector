from flask import Flask, render_template, request
from werkzeug import secure_filename
import PlateDetection as plate
import os
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './upload_images/'

app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/uploader', methods = ['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def uploader():
   if request.method == 'POST':
      if 'file' not in request.files:
         print("NAO TEM")
      else:
         f = request.files['file']
         f.save(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))

         p = plate.predict_car_plate(os.path.join(app.config['UPLOAD_FOLDER'],f.filename))

         return p
      return "ERRO"

if __name__ == '__main__':
   app.run(debug = True)
