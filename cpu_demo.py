import wikipedia
import networkx as nx
import random
import numpy as np
from utils import data_path, Network
import json
import matplotlib.pyplot as plt
import sys

model = [0] * 3000

class AccessCounter:
    accesses = []
    @classmethod
    def add_access(cls, obj):
        start = id(obj)
        # if len(cls.accesses) > 0 and start >= cls.accesses[-1] + 5e8:
        #     raise ValueError("Invalid memory access")
        address = [start + i for i in range(sys.getsizeof(obj))]
        cls.accesses += address

# Data structure to store processed pages
class PageStorage:
    def __init__(self):
        self.pages = {}  # Dictionary to store page title -> content
        self.neighbors = {}  # Dictionary to store page title -> list of neighbors
        self.access = [] # List to store the order of page access

        with open(data_path / "network.json") as f:
            network = Network.model_validate(json.load(f))
            for node in network.nodes:
                self.add_page(node, None)
                self.add_neighbors(node, network.links.get(node, []))

    def add_page(self, title, embedding):
        self.pages[title] = embedding

    def add_neighbors(self, title, neighbors):
        self.neighbors[title] = neighbors

    def get_embedding(self, title):
        if title in self.pages.keys():
            AccessCounter.add_access(self)
            AccessCounter.add_access(self.pages[title])
        return self.pages.get(title, None)

    def get_neighbors(self, title):
        if title in self.neighbors.keys():
            AccessCounter.add_access(self)
            AccessCounter.add_access(self.neighbors[title])
        return self.neighbors.get(title, [])
    
    def add_access(self, obj):
        self.access.append(id(obj))

# Placeholder for the LSTM embedding function
def lstm_embedding(text):
    # This function should be replaced with the actual LSTM embedding code
    # For demonstration, we'll return a random vector
    for i in text:
        AccessCounter.add_access(i)
    for param in model:
        AccessCounter.add_access(param)
    
    return np.random.rand(128)

# Function to process pages and calculate LSTM embeddings
def process_wikipedia_network(storage):
    visited_pages = set()
    
    # Start with the first page
    page_titles = list(storage.pages.keys())
    if not page_titles:
        return storage

    current_page = page_titles[0]

    while current_page:
        print(f"Processing page: {current_page}")
        # page_content = wikipedia.page(current_page).content
        page_content = "T" * 1000
        embedding = lstm_embedding(page_content)
        print(f"Generated embedding of shape: {embedding.shape}")

        # Store the page and its embedding
        # storage.add_page(current_page, embedding)
        # visited_pages.add(current_page)

        # Neighbors are assumed to be read from disk and stored already
        neighbors = storage.get_neighbors(current_page)
        if not neighbors:
            print(f"No neighbors found for {current_page}.")
            break

        # Choose one of the neighbors based on their titles
        unvisited_neighbors = [n for n in neighbors if n not in visited_pages]
        if not unvisited_neighbors:
            print(f"All neighbors visited for {current_page}.")
            break

        current_page = random.choice(unvisited_neighbors)

    return storage

# Example usage
if __name__ == "__main__":
    # Set random seed for reproducibility
    random.seed(1)
    # Simulated data, assuming pages and neighbors are read from disk
    storage = PageStorage()
    # storage.add_page("Artificial intelligence", None)
    # storage.add_neighbors("Artificial intelligence", ["Machine learning", "Neural network"])
    # storage.add_page("Machine learning", None)
    # storage.add_neighbors("Machine learning", ["Supervised learning", "Unsupervised learning"])
    # storage.add_page("Neural network", None)
    # storage.add_neighbors("Neural network", ["Deep learning", "Backpropagation"])
    # storage.add_page("Supervised learning", None)
    # storage.add_neighbors("Supervised learning", [])
    # storage.add_page("Unsupervised learning", None)
    # storage.add_neighbors("Unsupervised learning", [])
    # storage.add_page("Deep learning", None)
    # storage.add_neighbors("Deep learning", [])
    # storage.add_page("Backpropagation", None)
    # storage.add_neighbors("Backpropagation", [])

    storage = process_wikipedia_network(storage)

    # Example of accessing stored data
    # for title, embedding in storage.pages.items():
    #     if embedding is not None:
    #         print(f"Stored embedding for {title}: {embedding[:5]}...")
    # print(AccessCounter.accesses)


    # Sample memory addresses list (replace with your actual data)
    memory_accesses = AccessCounter.accesses  # List of memory addresses touched
    timestamps = np.arange(len(memory_accesses))  # Simulated time steps

    # Normalize memory addresses for better visualization
    # min_addr, max_addr = min(memory_accesses), max(memory_accesses)
    # normalized_addresses = [(addr - min_addr) / (max_addr - min_addr + 1) for addr in memory_accesses]

    # Scatter plot
    plt.figure(figsize=(10, 5))
    plt.scatter(timestamps, memory_accesses, alpha=0.6, s=10, c="blue")
    plt.xlabel("Time")
    plt.ylabel("Memory Address")
    # Do not use scientific notation for large numbers
    plt.ticklabel_format(style='plain', axis='y')
    # Use hex format for memory addresses
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: hex(int(x))))
    plt.title("Memory Access Pattern Over Time")
    print(hex(id(model[0])))
    plt.show()

