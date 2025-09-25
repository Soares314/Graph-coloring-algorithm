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

# Seleção dos grafos que vão reproduzir por roleta
def roulette_wheel_selection(evaluated_graphs, reproduction_rate):
    total_value = sum(evaluated_graphs.values())
    graphs_for_reproduction = []
    
    for _ in range(reproduction_rate * 2):
        pick = random.uniform(0, total_value)
        current = 0
        for graph, value in evaluated_graphs.items():
            current += value
            if current > pick:
                graphs_for_reproduction.append(graph)
                break
            
    return graphs_for_reproduction

# Algoritmo genético para decidir o grafo com melhor coloração
def color_graph(graph, number_colors, limit_of_generations):
    random_10_graphs = generate_random_colored_graphs(graph, number_colors, 10)
    evaluated_graphs = evaluate_colored_graphs(random_10_graphs)
    
    for node in evaluated_graphs:
        if evaluated_graphs[node] == graph.number_of_edges():
            return node

    graphs_for_reproduction = roulette_wheel_selection(evaluated_graphs, 1)
    

def main():
    G = nx.Graph([(0, 1), (1, 3),(1, 2), (2, 0), (0, 3)])

    color_graph(G, 3, 20)

main()