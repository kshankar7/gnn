"""
Basic reusable scripts for graph visualizations

email: kshankar@crimson.ua.edu
lab url: https://acmelab.ua.edu/
"""

import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph(adjacency_matrix, title="Graph Neural Network", save_path=None):
    """
    Visualize a graph represented by an adjacency matrix.

    Args:
        adjacency_matrix (torch.Tensor): Adjacency matrix representing the graph.
        title (str, optional): Title for the graph visualization. Default is "Graph Neural Network".
        save_path (str, optional): Path to save the visualization as an image file. Default is None.

    Returns:
        None
    """
    G = nx.DiGraph()
    num_nodes = adjacency_matrix.shape[0]
    G.add_nodes_from(range(1, num_nodes + 1))
    
    for i in range(num_nodes):
        for j in range(num_nodes):
            if adjacency_matrix[i][j] != 0:
                G.add_edge(i + 1, j + 1)

    # Draw the graph
    plt.figure(figsize=(6, 6))
    pos = nx.spring_layout(G)  # Layout for the nodes
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=10, font_weight='bold')

    plt.title(title)
    
    # Save the graph if save_path is provided
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()
    return save_path


def visualize_weights(weights_matrix, title="Weights Map", save_path=None):
    plt.imshow(weights_matrix)
    plt.title(title)
    if save_path:
        plt.savefig(save_path)
        plt.close()
    else:
        plt.show()
    return save_path

