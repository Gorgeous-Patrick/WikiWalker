from typing import Dict
from collections import defaultdict
from utils import Metadata, metadata_path, pagerank_path
import json


def compute_page_rank(
    metadata: Metadata, damping_factor: float = 0.85, iterations: int = 100
) -> Dict[str, float]:
    # Initialize the page rank dict with equal values
    link_data = metadata.link_data
    pages = link_data.keys()
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


def prep() -> Metadata:
    with open(metadata_path, "r") as file:
        parsed = json.load(file)
        return Metadata.model_validate(parsed)


def post(result: dict[str, float]):
    with open(pagerank_path, "w") as file:
        json.dump(result, file)


if __name__ == "__main__":
    metadata = prep()
    result = compute_page_rank(metadata, iterations=100)
    post(result)
