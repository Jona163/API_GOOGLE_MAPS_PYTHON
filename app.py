# Jona163
# Autor: Jonathan Hernández
# Fecha: 25 octubre de 2024 
# Proyecto: API GOOGLEMAPS
# GitHub: https://github.com/Jona163

from flask import Flask, request, render_template, jsonify
import googlemaps
import numpy as np
import random
import math

# Inicializa el cliente de Google Maps con tu API key
gmaps = googlemaps.Client(key='Apikey de google')
app = Flask(__name__)

# Obtiene las coordenadas GPS de una ciudad
def obtener_coordenadas(ciudad):
    geocode_result = gmaps.geocode(ciudad + ", Mexico")
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        return (location['lat'], location['lng'])
    else:
        return None

# Calcula la distancia entre dos puntos usando numpy
def distancia(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))
