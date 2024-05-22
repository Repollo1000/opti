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
                    instance.depot_node = int(line)
                else:
                    key, value = line.split(":")
                    setattr(instance, key.strip().lower(), value.strip())
    return instance

# Uso del código
filename = r"C:\Users\sebas\Desktop\1s2024\opti\Facil.vrp"

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
