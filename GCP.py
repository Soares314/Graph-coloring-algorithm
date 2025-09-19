import random
import networkx as nx

# Gera x grafos coloridos de forma aleátoria
def generate_random_colored_graphs(graph, number_colors, number_graphs):
    random_graphs = []

    for x in range(number_graphs):
        colored_graph = graph.copy()
        
        # Atribui uma cor aleatória para cada nó
        for node in colored_graph.nodes():
            colored_graph.nodes[node]['color'] = random.randint(0, number_colors - 1)
            
        random_graphs.append(colored_graph)
    
    return random_graphs

# Algoritmo genético para decidir o melhor grafo
def color_graph(graph, number_colors, limit_of_generations):
    random_10_graphs = generate_random_colored_graphs(graph, number_colors, 10)


def main():
    G = nx.Graph([(0, 1), (1, 2), (2, 0)])

    color_graph(G, 3, 20)

main()