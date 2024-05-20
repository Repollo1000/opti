import matplotlib.pyplot as plt
import numpy as np

# Clase para representar una instancia de CVRP
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

# Función para leer una instancia de CVRP desde un archivo
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

plt.scatter(x_coords[0], y_coords[0], color='blue', label='Nodo 1', s=node_size)  # Nodo 1 en color azul que sería la bodega
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
plt.show()

# Información adicional para la instancia
comentario = cvrp_instance.comment

# Dimension (número de clientes)
n = cvrp_instance.dimension

# Coordenadas de los nodos
node_coords = cvrp_instance.node_coords

# Demandas de los clientes
demands = cvrp_instance.demands

# Ajuste para el nodo 0 (depósito)
node_coords[0] = cvrp_instance.node_coords[1]  # Este ajuste puede no ser necesario, asegúrate de que sea correcto para tu caso

# Capacidad de los vehículos
Q = cvrp_instance.capacity

# Reorganización de las variables según la convención que tienes
N = list(range(1, n+1))
V = [0] + N
A = [(i, j) for i in V for j in V if i != j]
c = {(i, j): int(np.hypot(node_coords[i][0]-node_coords[j][0], node_coords[i][1]-node_coords[j][1])) for i, j in A}
q = {i: demands[i] for i in N}

# Imprimir los resultados para verificar
print("coordenadas del nodo 0:", node_coords[0])
print("n:", N)
print("v:", V)
print("A:", A)
print("Q:", Q)
print("c:", c)
print("q:", q)
