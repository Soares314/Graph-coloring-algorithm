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
    

# Crossover entre dois pais
def crossover(parent1, parent2):
    child = parent1.copy()
    for node in child.nodes():
        if random.random() < 0.5:
            child.nodes[node]['color'] = parent1.nodes[node]['color']
        else:
            child.nodes[node]['color'] = parent2.nodes[node]['color']
    return child

# Mutação em um grafo
def mutate(graph, number_colors, mutation_rate=0.1):
    for node in graph.nodes():
        if random.random() < mutation_rate:
            graph.nodes[node]['color'] = random.randint(0, number_colors - 1)
    return graph

# Algoritmo genético para decidir o grafo com melhor coloração
def color_graph(graph, number_colors, limit_of_generations):
    random_10_graphs = generate_random_colored_graphs(graph, number_colors, 10)
    
    for generation in range(limit_of_generations):
        evaluated_graphs = evaluate_colored_graphs(random_10_graphs)
        
        # Melhor grafo da geração
        best_graph = max(evaluated_graphs, key=evaluated_graphs.get)
        best_value = evaluated_graphs[best_graph]
        print(f"Geração {generation}: melhor valor = {best_value}")
        
        # Se já é solução ótima
        if best_value == graph.number_of_edges():
            print("Solução ótima encontrada!")
            return best_graph
        
        # Seleciona grafos para reprodução
        graphs_for_reproduction = roulette_wheel_selection(evaluated_graphs, 5)
        
        # Gera nova população com crossover + mutação
        new_population = []
        for i in range(0, len(graphs_for_reproduction), 2):
            if i + 1 < len(graphs_for_reproduction):
                child = crossover(graphs_for_reproduction[i], graphs_for_reproduction[i+1])
                child = mutate(child, number_colors)
                new_population.append(child)
        
        # Atualiza população
        if new_population:
            random_10_graphs = new_population
    
    return best_graph

def main():
    G = nx.Graph([(0, 1), (1, 3),(1, 2), (2, 0), (0, 3)])

    result = color_graph(G, 3, 20)
    print("Cores finais:")
    for node, data in result.nodes(data=True):
        print(f"Nó {node}: cor {data['color']}")

main()