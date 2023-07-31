# Importamos jsonify para manejar el JSON
from flask import Flask, request, jsonify
import os
import pickle
import zipfile
import requests

os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/", methods=['GET'])
def hello():
    return "Bienvenido a la API de temperaturas"


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
        return jsonify({"error": "Faltan argumentos en la llamada"})
    else:
        prediccion = model.predict([[ano, mes, dia, hora]])
        temperatura_prediccion = round(prediccion[0], 2)
        return jsonify({"Prediccion_temperatura_Madrid": temperatura_prediccion})


@app.route('/v1/temp_actual', methods=['GET'])
def temp():
    city = "Madrid"
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Madrid,es&appid={os.environ.get('API_KEY')}"
    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        temperature_kelvin = weather_data["main"]["temp"]
        temperature_celsius = temperature_kelvin - 273.15  # Convertir a Celsius
        temperature_data = {
            "city": city,
            "temperature_celsius": round(temperature_celsius, 2)
        }
        # Devolver la información en formato JSON
        return jsonify(temperature_data)
    else:
        error_data = {
            "error": "Error al obtener los datos meteorológicos."
        }
        return jsonify(error_data)  # Devolver mensaje de error en formato JSON


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)
