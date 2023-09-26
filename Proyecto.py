from flask import Flask, request
import pymongo
import requests

# Crear la aplicación Flask
app = Flask(__name__)

# Crear una conexión a MongoDB Atlas
client = pymongo.MongoClient("mongodb+srv://xChipics:Alejo2602*@cluster0.xslm9gv.mongodb.net/?retryWrites=true&w=majority")

# Crear la base de datos
db = client["my_database"]

# Crear la colección
collection = db["weather"]

# Obtener la clave de API
API_KEY = "1e9418b7cf357f292f9e4fbcc4aae0e5"

# Ruta para obtener la temperatura actual en una ciudad
@app.route("/temperature/<city>", methods=["GET"])
def get_temperature(city):

    # Obtener la temperatura de la API
    temperatura = get_temperature_from_api(city)

    # Devolver la temperatura con el nombre de la ciudad
    return {
        "city": city,
        "temperature": temperatura
    }

# Ruta para buscar ciudades por temperatura
@app.route("/search", methods=["GET"])
def search_cities():

    # Obtener la temperatura mínima y máxima
    temperatura_minima = float(request.args.get("temperatura_minima"))
    temperatura_maxima = float(request.args.get("temperatura_maxima"))

    # Consultar la colección
    cursor = collection.find({"temperature": {"$gt": temperatura_minima, "$lt": temperatura_maxima}})

    # Devolver los resultados
    for document in cursor:
        return document

# Ruta para obtener la temperatura de 3 ciudades
@app.route("/three_cities", methods=["GET"])
def three_cities():

    # Obtener las 3 ciudades
    ciudades = ["Quito,ec", "Guayaquil,ec", "Cuenca,ec"]

    # Obtener las temperaturas
    temperaturas = []
    for ciudad in ciudades:
        # Obtener la temperatura de la API
        temperatura = get_temperature_from_api(ciudad)
        temperaturas.append(temperatura)

    # Devolver las temperaturas
    return temperaturas

# Obtener la temperatura actual de las 3 ciudades más importantes de Ecuador
def get_temperature_from_api(city):

    # Obtener la URL de la API
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + API_KEY + "&units=metric"

    # Realizar la petición a la API
    response = requests.get(url)

    # Convertir la respuesta a JSON
    data = response.json()

    # Obtener el nombre de la ciudad
    city_name = data["name"]

    # Obtener la temperatura en Celsius
    temperatura_celsius = data["main"]["temp"]

    # Obtener la presión
    pressure = data["main"]["pressure"]

    # Obtener la humedad
    humidity = data["main"]["humidity"]

    # Obtener la velocidad del viento
    wind_speed = data["wind"]["speed"]

    # Devolver el diccionario con todos los valores

    return {
        "Ciudad": city_name,
        "Temperatura": temperatura_celsius,
        "Presion": pressure,
        "Humedad": humidity,
        "Velocidad del viento": wind_speed
    }

# Iniciar la aplicación
app.run()
