import matplotlib.pyplot as plt

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
                    depot_info = line.split()
                    if len(depot_info) > 0:
                        instance.depot_node = int(depot_info[0])
    return instance

def plot_cvrp_instance(instance):
    depot_node = instance.depot_node
    if depot_node == -1:  # Si el depósito está configurado como -1, buscar el nodo con demanda cero
        for node, demand in instance.demands.items():
            if demand == 0:
                depot_node = node
                break
    depot_coords = instance.node_coords[depot_node]

    plt.figure(figsize=(8, 8))
    plt.scatter(*zip(*instance.node_coords.values()), color='b', label='Clientes')
    plt.scatter(*depot_coords, color='r', label='Depósito')

    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.title('Instancia CVRP: {}'.format(instance.name))
    plt.legend()
    plt.grid(True)
    plt.show()


# Uso del código
filename = r"Dificil.vrp"

instance = read_cvrp_instance(filename)

# Ejemplo de acceso a los datos leídos
print("Nombre:", instance.name)
print("Tipo:", instance.type)
print("Comentario:", instance.comment)
print("Dimensión:", instance.dimension)
print("Capacidad:", instance.capacity)
print("Tipo de peso de arista:", instance.edge_weight_type)
print("Coordenadas de los nodos:", instance.node_coords)
print("Demandas de los nodos:", instance.demands)
print("Nodo del depósito:", instance.depot_node)



plot_cvrp_instance(instance)

