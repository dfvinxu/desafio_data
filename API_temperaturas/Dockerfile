# Para que nuestra imagen se base en python 
FROM python:3.11.4

# Creación de una carpeta donde meter el código fuente de nuestra aplicación. Esta carpeta no hace referencia a la maquina física, sino es en base al contenedor.
WORKDIR /app

# Indicar al contenedor de donde va a extraer el código
COPY . /app

RUN pip install -r requirements.txt

# Variables de entorno
ENV API_KEY="2a4888d5bb0e8e262434c0d42226a16e"
ENV PORT=5000

# El puerto
EXPOSE $PORT

# Para que corra la aplicación.
CMD ["python", "/app/app.py"]
