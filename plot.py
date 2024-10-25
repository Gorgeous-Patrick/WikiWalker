import networkx as nx
import matplotlib.pyplot as plt
from utils import Metadata, metadata_path
import json
import random

def count_edge(paths: list[list[str]]):
    count = {}
    for path in paths:
        for i in range(len(path) - 1):
            edge = (min(path[i], path[i + 1]), max(path[i],path[i+1]))
            edge_count = count.get(edge, 0)
            count[edge] = edge_count + 1

    return count

# Function to draw the directed graph
def draw_graph(metadata: Metadata, paths: list[list[str]]):
    # Create a directed graph
    graph = nx.DiGraph()

    # Add edges from the link_data
    for node, edges in metadata.link_data.items():
        for edge in edges:
            if edge in metadata.link_data.keys():
                graph.add_edge(node, edge)
    # Draw the graph with labels
    pos = nx.kamada_kawai_layout(graph, scale=2.0)  # Positioning of nodes
    nx.draw(
        graph,
        pos,
        with_labels=False,
        node_size=500,
        font_size=5,
        font_color="white",
        font_weight="bold",
        edge_color="gray",
        arrows=False,
    )

    print(len(paths))

    for path_to_highlight in range(len(paths)):
        colors = ["red", "green", "blue", "violet", "gray", "purple", "orange", "yellow"]
        # Get the specific path to highlight (convert it to edges)
        path_edges = [
            (paths[path_to_highlight][i], paths[path_to_highlight][i + 1])
            for i in range(len(paths[path_to_highlight]) - 1)
        ]

        # Highlight the specific path by drawing it with a different color and width
        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist=path_edges,
            edge_color=colors[
                path_to_highlight % len(colors)
            ],  # Highlighted edge color
            width=2.5,  # Highlighted edge thickness
        )

    # Show the graph
    plt.show()

def hist(paths: list[list[str]]):
    # Count edges
    edge_counts = count_edge(paths)
    
    # Prepare the data for histogram
    counts = list(edge_counts.values())
    
    # Plot histogram
    print(counts)
    plt.hist(counts, edgecolor='black')
    plt.title('Distribution of Edge Visit Counts')
    plt.xlabel('Number of Visits')
    plt.ylabel('Frequency of Edges')
    plt.show()


def prep() -> Metadata:
    with open(metadata_path, "r") as file:
        parsed = json.load(file)
        return Metadata.model_validate(parsed)


if __name__ == "__main__":
    metadata = prep()
    with open("result.json", "r") as result_file:
        paths = json.load(result_file)
        draw_graph(metadata, paths)
        hist(paths)
