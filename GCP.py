import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

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

# Plota o grafo colorido
def plot_colored_graph(graph, title, ax):
    pos = nx.spring_layout(graph)
    
    # Mapeia cores para valores RGB
    color_map = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'brown', 'pink']
    node_colors = [color_map[graph.nodes[node]['color']] for node in graph.nodes()]
    
    nx.draw(graph, pos, ax=ax, with_labels=True, node_color=node_colors, 
            node_size=500, font_size=16, font_weight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')

def main():
    
    # Grafos Entrada
    G0 = nx.Graph([(0, 1), (0, 2),(2, 3), (1, 3)])
    G1 = nx.Graph([(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 6), (2, 7), (3, 8), (3, 9), (4,5), (6,7), (8,9)])
    G2 = nx.Graph([(0,1),(0,4),(0,5),(0,6),(1,2),(1,5),(1,7),(2,3),(2,6),(2,8),(3,4),(3,7),(3,9),(4,5),(4,8),(4,10),(5,9),(5,11),(6,7),(6,10),(6,12),(7,11),(7,13),(8,9),(8,12),(8,14),(9,13),(9,15),(10,11),(10,14),(10,16),(11,15),(11,17),(12,13),(12,16),(12,18),(13,17),(13,19),(14,15),(14,18),(15,19),(16,17),(17,18),(18,19)])

    # Grafos Saída
    GC0 = color_graph(G0, 2, 100)
    GC1 = color_graph(G1, 3, 200)
    GC2 = color_graph(G2, 5, 10000)
    
    # Plota os três grafos coloridos
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    plot_colored_graph(GC0, 'Grafo GC0 (2 cores)', axes[0])
    plot_colored_graph(GC1, 'Grafo GC1 (3 cores)', axes[1]) 
    plot_colored_graph(GC2, 'Grafo GC2 (5 cores)', axes[2])

    plt.tight_layout()
    plt.show()

main()