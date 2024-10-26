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

# Algoritmo de Dijkstra
def dijkstra(graph, initial):
    visited = {initial: 0}
    path = {}

    nodes = set(graph.keys())

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node

        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph[min_node]:
            weight = current_weight + graph[min_node][edge]
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path

# Búsqueda Tabú
def busqueda_tabu(graph, start, end, tabu_size=10, max_iter=100):
    current_node = start
    best_path = [start]
    tabu_list = set()
    best_distance = float('inf')

    for _ in range(max_iter):
        neighbors = graph[current_node]
        next_node = None

        for neighbor in neighbors:
            if neighbor not in tabu_list and (next_node is None or neighbors[neighbor] < neighbors[next_node]):
                next_node = neighbor

        if next_node is None:
            break

        best_path.append(next_node)
        tabu_list.add(next_node)

        if len(tabu_list) > tabu_size:
            tabu_list.remove(best_path[-tabu_size - 1])

        current_node = next_node

        if current_node == end:
            total_distance = sum(graph[best_path[i]][best_path[i + 1]] for i in range(len(best_path) - 1))
            if total_distance < best_distance:
                best_distance = total_distance

    return best_path, best_distance
# Algoritmo Genético Mejorado con Criterios de Cauchy y Boltzmann
def algoritmo_genetico_mejorado(graph, start, end, population_size=100, generations=500, crossover_rate=0.8, mutation_rate=0.02, elitism=True):
    def create_individual():
        individual = list(graph.keys())
        random.shuffle(individual)
        return individual

    def fitness(individual):
        total_distance = 0
        for i in range(len(individual) - 1):
            total_distance += graph[individual[i]][individual[i + 1]]
        return total_distance
