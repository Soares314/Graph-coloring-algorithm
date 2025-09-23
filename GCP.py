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

#Avalia os grafos pela quantidade de arestas cujo os nós tem cores diferentes 
def evaluate_colored_graphs(colored_graphs):
    colored_graphs_evaluated = {}
    
    for graph in colored_graphs:
        graph_value = 0
        
        # Para cada dois nós ligados, verifica se tem cores diferente, se sim o grafo ganha mais valor
        for node1, node2 in graph.edges():
            if graph.nodes[node1]['color'] != graph.nodes[node2]['color']:
                graph_value += 1
                    
        colored_graphs_evaluated.update({graph: graph_value})
    
    return colored_graphs_evaluated
        

# Algoritmo genético para decidir o grafo com melhor coloração
def color_graph(graph, number_colors, limit_of_generations):
    print(graph.number_of_edges())
    
    random_10_graphs = generate_random_colored_graphs(graph, number_colors, 10)
    evaluated_graphs = evaluate_colored_graphs(random_10_graphs)
    
    print("Coloração ideal do grafo:")
    for node in evaluated_graphs:
        if evaluated_graphs[node] == graph.number_of_edges():
            return node

def main():
    G = nx.Graph([(0, 1), (1, 3),(1, 2), (2, 0), (0, 3)])

    color_graph(G, 3, 20)

main()