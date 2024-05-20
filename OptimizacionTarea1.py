#Integrantes:

#Sebastian Soza Madariaga 20677990-K
#Sofia Labra Bustamante 20885828-9
#Maite Villalon Palma 20731482-K
import matplotlib.pyplot as plt
from gurobipy import Model, GRB, quicksum
import numpy as np

# Función para leer la instancia CVRP
class CVRPInstance:
    def __init__(self, name, comment, type_, dimension, edge_weight_type, capacity, node_coords, demands):
        self.name = name
        self.comment = comment
        self.type = type_
        self.dimension = dimension
        self.edge_weight_type = edge_weight_type
        self.capacity = capacity
        self.node_coords = node_coords
        self.demands = demands

def read_cvrp_instance(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    instance_data = {}
    node_coords = {}
    demands = {}

    node_coord_section = False
    demand_section = False

    for line in lines:
        line = line.strip()
        print("Línea leída:", line)
        if line.startswith("NAME"):
            instance_data["name"] = line.split(":")[1].strip()
        elif line.startswith("COMMENT"):
            instance_data["comment"] = line
        elif line.startswith("TYPE"):
            instance_data["type"] = line.split(":")[1].strip()
        elif line.startswith("DIMENSION"):
            instance_data["dimension"] = int(line.split(":")[1])
        elif line.startswith("EDGE_WEIGHT_TYPE"):
            instance_data["edge_weight_type"] = line.split(":")[1].strip()
        elif line.startswith("CAPACITY"):
            instance_data["capacity"] = int(line.split(":")[1])
        elif line.startswith("NODE_COORD_SECTION"):
            node_coord_section = True
            continue
        elif line.startswith("DEMAND_SECTION"):
            node_coord_section = False
            demand_section = True
            continue
        elif line.startswith("DEPOT_SECTION"):
            demand_section = False
            continue
        elif line.startswith("EOF"):
            break
        elif node_coord_section:
            parts = line.split()
            node_coords[int(parts[0])] = (float(parts[1]), float(parts[2]))
        elif demand_section:
            parts = line.split()
            demands[int(parts[0])] = int(parts[1])

    return CVRPInstance(instance_data["name"], instance_data["comment"], instance_data["type"], instance_data["dimension"],
                        instance_data["edge_weight_type"], instance_data["capacity"], node_coords, demands)

# Ruta al archivo de instancia CVRP
file_path = "Facil.vrp"
# Llamar a la función para leer la instancia CVRP
cvrp_instance = read_cvrp_instance(file_path)

# Extraer las coordenadas de los nodos
node_coords = cvrp_instance.node_coords
demanda = cvrp_instance.demands

# Crear listas separadas para las coordenadas x e y de los nodos
x_coords = [coord[0] for coord in node_coords.values()]
y_coords = [coord[1] for coord in node_coords.values()]

# Graficar las coordenadas de los nodos
plt.figure(figsize=(20, 12))

node_size = 250

plt.scatter(x_coords[0], y_coords[0], color='blue', label='Nodo 1', s=node_size)  # Nodo 1 en color rojo que sería la bodega
plt.scatter(x_coords[1:], y_coords[1:], color='red', label='Otros nodos', s=node_size)

# Agregar etiquetas a los nodos
for i, (x, y) in enumerate(node_coords.values()):
    node_number = i + 1  # Incrementar el número de nodo en 1 para coincidir con las claves en "demanda"
    demand = demanda[node_number]  # Obtener la demanda del nodo actual
    plt.text(x, y, str(demand), fontsize=8, ha='center', va='center', color='white')

# Configurar etiquetas y título del gráfico
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.title('Grafico de Coordenadas de los Nodos')

# Mostrar leyenda
plt.legend()

# Mostrar el gráfico
plt.grid(True)


# Comentario
comentario = cvrp_instance.comment

# Dimension (número de clientes)
n = cvrp_instance.dimension

# Coordenadas de los nodos
node_coords = cvrp_instance.node_coords

# Demandas de los clientes
demands = cvrp_instance.demands

node_coords[0] = cvrp_instance.node_coords[1]

print("coordenadas", node_coords[0])
# Capacidad de los vehículos
Q = cvrp_instance.capacity

# Reorganización de las variables según la convención que tienes
N = list(range(1, n+1))
V = [0] + N
A = [(i, j) for i in V for j in V if i != j]
c = {(i, j): int(np.hypot(node_coords[i][0]-node_coords[j][0], node_coords[i][1]-node_coords[j][1])) for i, j in A}
q = {i: demands[i] for i in N}

print("n:",N)
print("v:",V)
print("A:",A)
print("Q:",Q)
print("c:",c)
print("q:",q)

rnd = np.random
rnd.seed(0)
plt.figure(figsize=(10, 6))
# Crear modelo CVRP con Gurobi
mdl = Model('CVRP')
x = mdl.addVars(A, vtype=GRB.BINARY)
u = mdl.addVars(N, vtype=GRB.CONTINUOUS)
mdl.modelSense = GRB.MINIMIZE
mdl.setObjective(quicksum(x[i, j]*c[i, j] for i, j in A))

mdl.addConstrs(quicksum(x[i, j] for j in V if j != i) == 1 for i in N)
mdl.addConstrs(quicksum(x[i, j] for i in V if i != j) == 1 for j in N)
mdl.addConstrs((x[i, j] == 1) >> (u[i]+q[j] == u[j])
               for i, j in A if i != 0 and j != 0)
mdl.addConstrs(u[i] >= q[i] for i in N)
mdl.addConstrs(u[i] <= Q for i in N)

mdl.Params.MIPGap = 0.1
mdl.Params.TimeLimit = 200
mdl.optimize()

active_arcs = [(i, j) for (i, j) in A if x[i, j].x > 0.99]

for i, j in active_arcs:
    plt.plot([node_coords[i][0], node_coords[j][0]], [node_coords[i][1], node_coords[j][1]], c='g', zorder=0)

plt.scatter([node_coords[i][0] for i in range(len(node_coords))], [node_coords[i][1] for i in range(len(node_coords))], c='b')

plt.scatter(node_coords[1][0], node_coords[1][1], c='r', marker='s')

#plt.show()

# Imprimir el costo óptimo
print("Costo óptimo de la solución:", mdl.objVal)


import matplotlib.pyplot as plt

# Colores disponibles para las rutas
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# Diccionario para almacenar las rutas de cada vehículo
vehicle_routes = {}

# Obtener las rutas de cada vehículo
for i, j in active_arcs:
    if i != 0 and j != 0:
        if i not in vehicle_routes:
            vehicle_routes[i] = []
        vehicle_routes[i].append(j)

# Graficar las rutas de cada vehículo con colores diferentes
for idx, (vehicle, route) in enumerate(vehicle_routes.items()):
    color = colors[idx % len(colors)]  # Seleccionar un color de la lista de colores
    for k in range(len(route) - 1):
        i, j = route[k], route[k + 1]
        plt.plot([node_coords[i][0], node_coords[j][0]], [node_coords[i][1], node_coords[j][1]], c=color, zorder=0)

# Graficar los nodos
plt.scatter([node_coords[i][0] for i in range(len(node_coords))], [node_coords[i][1] for i in range(len(node_coords))], c='b')

# Marcar el nodo inicial en rojo
plt.scatter(node_coords[1][0], node_coords[1][1], c='r', marker='s')

# Mostrar el gráfico
#plt.show()


# Colores disponibles para las rutas
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# Diccionario para almacenar las rutas de cada vehículo
vehicle_routes = {}

# Obtener las rutas de cada vehículo
for i, j in active_arcs:
    if i != 0 and j != 0:
        if i not in vehicle_routes:
            vehicle_routes[i] = []
        vehicle_routes[i].append(j)

# Graficar las rutas de cada vehículo con colores diferentes y guardar las rutas
for idx, (vehicle, route) in enumerate(vehicle_routes.items()):
    color = colors[idx % len(colors)]  # Seleccionar un color de la lista de colores
    for k in range(len(route) - 1):
        i, j = route[k], route[k + 1]
        plt.plot([node_coords[i][0], node_coords[j][0]], [node_coords[i][1], node_coords[j][1]], c=color, zorder=0)
        
    # Guardar la ruta del vehículo
    vehicle_routes[vehicle] = route

# Graficar los nodos
plt.scatter([node_coords[i][0] for i in range(len(node_coords))], [node_coords[i][1] for i in range(len(node_coords))], c='b')

# Marcar el nodo inicial en rojo
plt.scatter(node_coords[1][0], node_coords[1][1], c='r', marker='s')

# Mostrar el gráfico
plt.show()

# Imprimir las rutas de cada vehículo
#for vehicle, route in vehicle_routes.items():
#    print(f"Ruta del vehículo {vehicle}: {route}")