from flask import Flask, request
import os
import pickle
import zipfile


os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=['GET'])
def hello():
    return "Bienvenido a la API de predicción de temperaturas"

@app.route('/v1/predict', methods=['GET'])
def predict():

    zip_file_path = "./model/model_temp.zip"
    model_file_path = "model_temp.pkl"
    
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        with zip_file.open(model_file_path) as model_file:
            model = pickle.load(model_file)
    
    ano = request.args.get('ano', None)
    mes = request.args.get('mes', None)
    dia = request.args.get('dia', None)
    hora = request.args.get('hora', None)

    if ano is None or mes is None or dia is None or hora is None:
        return "Faltan argumentos en la llamada"
    else:
        prediccion = model.predict([[ano, mes, dia, hora]])
        return "Predicción de temperatura en Madrid:" + str(round(prediccion[0],2)) + 'ºC'
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)