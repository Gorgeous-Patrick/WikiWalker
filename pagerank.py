from typing import Dict
from collections import defaultdict
from utils import Network, network_path, pagerank_path
import json


def compute_page_rank(
    network: Network, damping_factor: float = 0.85, iterations: int = 100
) -> Dict[str, float]:
    # Initialize the page rank dict with equal values
    link_data = network.links
    pages = network.nodes
    n = len(pages)

    if n == 0:
        return {}

    page_rank = {page: 1 / n for page in pages}

    # Create a reverse link structure
    incoming_links = defaultdict(list)
    for page, out_links in link_data.items():
        for out_link in out_links:
            incoming_links[out_link].append(page)

    # Run PageRank iterations
    for _ in range(iterations):
        new_page_rank = {}
        for page in pages:
            rank_sum = sum(
                page_rank[in_page] / len(link_data[in_page])
                for in_page in incoming_links[page]
                if in_page in link_data and len(link_data[in_page]) > 0
            )
            new_page_rank[page] = (1 - damping_factor) / n + damping_factor * rank_sum
        page_rank = new_page_rank

    return page_rank


def prep():
    with open(network_path, "r") as file:
        parsed = json.load(file)
        return Network(**parsed)


def post(result):
    with open(pagerank_path, "w") as file:
        file.write(json.dumps(result))


if __name__ == "__main__":
    network = prep()
    result = compute_page_rank(network, iterations=100)
    print(result)
    post(result)
