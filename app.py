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
gmaps = googlemaps.Client(key='AIzaSyDytpSLPygjIvXWahgD6BABOeMx6VUTQqU')
