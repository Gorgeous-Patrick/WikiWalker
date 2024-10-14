import wikipediaapi
import json
import os
from utils import Metadata, metadata_path, data_path


wiki_wiki = wikipediaapi.Wikipedia("Jaseci Lab University of Michigan", "en")

start = "Conflict-driven_clause_learning"

def prep() -> Metadata:
    if not data_path.exists():
        os.makedirs(data_path)
    if metadata_path.exists():
        with open(metadata_path, "r") as file:
            parsed = json.load(file)
            return Metadata.model_validate(parsed)
    else:
        return Metadata(queue=[start], visited=[], link_data={})


def fetch(name: str):
    page = wiki_wiki.page(name)
    # print(f"Fetching {name}")
    return list(page.links)


def post(metadata: Metadata):
    with open(metadata_path, "w") as file:
        file.write(metadata.model_dump_json())


def expand(
    frontier: list[str], data: dict[str, list[str]], visited: list[str], size: int
):
    new_data = {}
    while len(frontier) > 0:
        name = frontier.pop(0)
        print(f"Working on {name}")
        links = fetch(name)
        links_filtered = [link for link in links if ":" not in link and link not in visited][:10]
        visited.extend(links_filtered)
        new_data[name] = links_filtered
        frontier.extend(links_filtered)
        # print("FRONTIER", frontier)
        data.update(new_data)
        # print(len(new_data))
        if len(new_data) >= size:
            break


if __name__ == "__main__":
    metadata = prep()
    while True:
        expand(metadata.queue, metadata.link_data, metadata.visited, 100)
        # print("NEW", frontier)
        post(metadata)
        print(f"WRITE: {len(metadata.link_data)} Pages expanded")
