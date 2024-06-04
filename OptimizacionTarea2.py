import math
import random

class CVRPInstance:
    def __init__(self):
        self.name = None
        self.type = None
        self.comment = None
        self.dimension = None
        self.capacity = None
        self.edge_weight_type = None
        self.node_coords = {}
        self.demands = {}
        self.depot_node = None

def read_cvrp_instance(filename):
    instance = CVRPInstance()
    with open(filename, 'r') as file:
        section = None
        for line in file:
            line = line.strip()
            if line == "NODE_COORD_SECTION":
                section = "NODE_COORD_SECTION"
            elif line == "DEMAND_SECTION":
                section = "DEMAND_SECTION"
            elif line == "DEPOT_SECTION":
                section = "DEPOT_SECTION"
            elif line == "EOF":
                break
            else:
                if section == "NODE_COORD_SECTION":
                    node_id, x, y = map(int, line.split())
                    instance.node_coords[node_id] = (x, y)
                elif section == "DEMAND_SECTION":
                    node_id, demand = map(int, line.split())
                    instance.demands[node_id] = demand
                elif section == "DEPOT_SECTION":
                    depot_node = int(line)
                    if depot_node != -1:
                        instance.depot_node = depot_node
                else:
                    key, value = line.split(":")
                    if key.strip().lower() in ["dimension", "capacity"]:
                        setattr(instance, key.strip().lower(), int(value.strip()))
                    else:
                        setattr(instance, key.strip().lower(), value.strip())
    
    if instance.depot_node is None:
        raise ValueError("El nodo del depósito no se ha especificado correctamente.")
    return instance

# Uso del código
filename = r"Facil.vrp"

instance = read_cvrp_instance(filename)

# Ejemplo de acceso a los datos leídos

print("----Lectura Datos Instancia------")
print("Nombre:", instance.name)
print("Tipo:", instance.type)
print("Comentario:", instance.comment)
print("Dimensión:", instance.dimension)
print("Capacidad:", instance.capacity)
print("Tipo de peso de arista:", instance.edge_weight_type)
print("Coordenadas de los nodos:", instance.node_coords)
print("Demandas de los nodos:", instance.demands)
print("Nodo del depósito:", instance.depot_node)
print("-----------------------------------")

import matplotlib.pyplot as plt

def plot_nodes(instance):
    depot_coords = instance.node_coords[instance.depot_node]
    other_coords = [coord for node, coord in instance.node_coords.items() if node != instance.depot_node]

    plt.figure(figsize=(8, 6))
    plt.scatter(*zip(*other_coords), color='blue', label='Nodos')
    plt.scatter(*zip(depot_coords), color='red', label='Depósito')
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.title('Ubicación de los nodos')
    plt.legend()
    plt.grid(True)
    plt.show()

# Uso
plot_nodes(instance)


#Heuristica vecino mas cercano
# Función que calcula la distancia euclidiana entre dos coordenadas
def distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

# Genera una solución inicial utilizando la heurística del Vecino Más Cercano
def nearestNeighbor(instance):
    #nodos no visitados
    unvisited = set(instance.node_coords.keys()) - {instance.depot_node}
    #nodo actual, parte en deposito
    current_node = instance.depot_node
    rutas = []
    ruta = []
    #carga actual del vehiculo
    current_load = 0

    while unvisited:
        nearest_node = None
        #distancia minima recorrida, parte en infinito
        nearest_distance = float('inf')

        # Encontrar el cliente más cercano que no exceda la capacidad del vehículo
        for node in unvisited:
            if current_load + instance.demands[node] <= instance.capacity:
                dist = distance(instance.node_coords[current_node], instance.node_coords[node])
                if dist < nearest_distance:
                    nearest_distance = dist
                    nearest_node = node

        if nearest_node is None:
            # Si no se puede agregar ningún cliente adicional, cerrar la ruta y empezar una nueva
            rutas.append(ruta + [instance.depot_node])
            ruta = []
            current_load = 0
            current_node = instance.depot_node
        else:
            # Agrego el cliente más cercano a la ruta actual
            ruta.append(nearest_node)
            current_load += instance.demands[nearest_node]
            current_node = nearest_node
            unvisited.remove(nearest_node)

    if ruta:
        # Agrego la última ruta si no está vacía
        rutas.append(ruta + [instance.depot_node])

    return rutas

solucionInicial = nearestNeighbor(instance)

# Generar la solución inicial utilizando la heurística del Vecino Más Cercano
solucionInicial = nearestNeighbor(instance)

def contar_camiones(solucion):
    return len(solucion)

cantidad_camiones = contar_camiones(solucionInicial)
print("Cantidad de camiones utilizados:", cantidad_camiones)

print("----HEURISTICA VECINO MAS CERNAO------")
print("La solución del vecino más cercano es:", solucionInicial)
print("-----------------------------------")


import matplotlib.pyplot as plt

def plot_nodes_with_route(instance, routes):
    depot_coords = instance.node_coords[instance.depot_node]
    other_coords = [coord for node, coord in instance.node_coords.items() if node != instance.depot_node]

    plt.figure(figsize=(8, 6))
    plt.scatter(*zip(*other_coords), color='blue', label='Nodos')
    plt.scatter(*zip(depot_coords), color='red', label='Depósito')

    # Dibujar todas las rutas
    for route in routes:
        for i in range(len(route)):
            node1 = route[i]
            node2 = route[(i + 1) % len(route)]
            coords1 = instance.node_coords[node1]
            coords2 = instance.node_coords[node2]
            plt.plot([coords1[0], coords2[0]], [coords1[1], coords2[1]], color='green', linewidth=1)

    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.title('Rutas iniciales del Vecino más cercano')
    plt.legend()
    plt.grid(True)
    plt.show()

# Uso
plot_nodes_with_route(instance, solucionInicial)


# Uso
plot_nodes_with_route(instance, solucionInicial[0])  # Solo mostramos la primera ruta generada por la heurística


#Calcular el costo de una ruta dada

def calcularCosto(instance, solucion ):
    costoTotal = 0
    for ruta in solucion:
        costoRuta = 0
        for i in range(len(ruta) - 1):
            costoRuta+= distance(instance.node_coords[ruta[i]], instance.node_coords[ruta[i + 1]])
        costoTotal += costoRuta
    return costoTotal

#Generamos una solucion vecino con 2-opt

def two_Opt(ruta):
    mejorRuta = ruta
    mejorCosto = calcularCosto(instance, ruta)
    improved = True

    while improved:
        improved = False
        for i in range(1, len(ruta)-2):
            for j in range(i+1, len(ruta)-1):
                if j-i == 1: continue #No intercambia aristas adyacentes
                nuevaRuta = ruta[:i] + ruta[i:j+1][::-1] + ruta[j+1:]
                nuevoCosto = calcularCosto(instance, nuevaRuta)
                if nuevoCosto < mejorCosto:
                    mejorRuta = nuevaRuta
                    mejorCosto = nuevoCosto
                    improved = True
                    ruta = mejorRuta  # Update the original route
    return mejorRuta
          



