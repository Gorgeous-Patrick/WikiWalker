# Construct Network class with nodes and links fields.

from utils import Network, PageInfo, cache_path, network_path
import json
import os

def read_cache(file_name: str) -> PageInfo:
    with open(cache_path / file_name, "r") as file:
        parsed = json.load(file)
        return PageInfo(**parsed)

def all_pages_files() -> list[str]:
    return [f for f in os.listdir(cache_path) if os.path.isfile(cache_path / f)]

def construct_network() -> Network:
    files = all_pages_files()
    nodes = set()
    links = {}
    for file in files:
        page = read_cache(file)
        nodes.add(page.title)
    for file in files:
        page = read_cache(file)
        links[page.title] = [link for link in page.links if link in nodes]
    return Network(nodes=nodes, links=links)

def avg_degree(network: Network) -> float:
    return sum([len(links) for links in network.links.values()]) / len(network.nodes)

def post(network: Network):
    with open(network_path, "w") as file:
        file.write(network.model_dump_json())

def main():
    network = construct_network()
    print(avg_degree(network))
    post(network)

if __name__ == "__main__":
    main()
