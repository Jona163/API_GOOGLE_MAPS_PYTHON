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

    def crossover(parent1, parent2):
        if random.random() > crossover_rate:
            return parent1, parent2
        cross_point = random.randint(1, len(parent1) - 2)
        child1 = parent1[:cross_point] + [gene for gene in parent2 if gene not in parent1[:cross_point]]
        child2 = parent2[:cross_point] + [gene for gene in parent1 if gene not in parent2[:cross_point]]
        return child1, child2

    def mutate(individual):
        if random.random() < mutation_rate:
            idx1, idx2 = random.sample(range(len(individual)), 2)
            individual[idx1], individual[idx2] = individual[idx2], individual[idx1]

    def boltzmann_probability(old_cost, new_cost, temperature):
        if new_cost < old_cost:
            return 1.0
        return math.exp((old_cost - new_cost) / temperature)

    population = [create_individual() for _ in range(population_size)]
    best_individual = None
    best_fitness = float('inf')

    for generation in range(generations):
        temperature = max(1.0, float(generations - generation) / generations)  # Temperatura Boltzmann
        new_population = []

        population = sorted(population, key=fitness)
        
        if fitness(population[0]) < best_fitness:
            best_individual = population[0]
            best_fitness = fitness(population[0])

        # Elitismo
        if elitism:
            new_population.append(population[0])

        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population, k=2)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1)
            mutate(child2)

            # Criterio de Boltzmann para aceptar nuevos individuos
            for child in [child1, child2]:
                if random.random() < boltzmann_probability(fitness(parent1), fitness(child), temperature):
                    new_population.append(child)

        population = new_population

    return best_individual, best_fitness

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ruta', methods=['POST'])
def calcular_ruta():
    ciudad_origen = request.form['origen']
    ciudad_destino = request.form['destino']
    
    coordenadas_origen = obtener_coordenadas(ciudad_origen)
    coordenadas_destino = obtener_coordenadas(ciudad_destino)
    
    if coordenadas_origen and coordenadas_destino:
        # Crear el grafo
        ciudades = ["Ciudad de Mexico", "Guadalajara", "Monterrey", "Puebla", "Tijuana"]
        grafo = {}
        for ciudad in ciudades:
            coordenadas = obtener_coordenadas(ciudad)
            if coordenadas:
                grafo[ciudad] = {}

        for ciudad1 in grafo:
            for ciudad2 in grafo:
                if ciudad1 != ciudad2:
                    grafo[ciudad1][ciudad2] = distancia(obtener_coordenadas(ciudad1), obtener_coordenadas(ciudad2))
        
