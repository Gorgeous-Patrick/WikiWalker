import wikipediaapi
import json
import os
from utils import Metadata, metadata_path, data_path
from pydantic import BaseModel


class PageInfo(BaseModel):
    title: str
    text: str
    links: list[str]


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


# Read the disk file if it exists, otherwise create the page file and download it from wikipedia
def fetch_and_save(name: str) -> PageInfo:
    cache_path = data_path / "cache"
    if not cache_path.exists():
        os.makedirs(cache_path)
    file_name = name.replace("/", "_")
    if (cache_path / f"{file_name}.json").exists():
        # Escape the file if it already exists
        # Escape the path invalid characters
        with open(cache_path / f"{file_name}.json", "r") as file:
            parsed = json.load(file)
            return PageInfo(**parsed)
    else:
        page = wiki_wiki.page(name)
        parsed = PageInfo(title=page.title, text=page.text, links=list(page.links))
        with open(cache_path / f"{file_name}.json", "w") as file:
            file.write(parsed.model_dump_json())
            return parsed


def filter_topic(name: str):
    page = fetch_and_save(name)
    return "satisfiability" in page.text


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
        links = fetch_and_save(name).links
        links_filtered = [
            link for link in links if ":" not in link and filter_topic(link)
        ]
        frontier.extend([link for link in links_filtered if link not in visited])
        visited.extend(links_filtered)
        new_data[name] = links_filtered
        # print("FRONTIER", frontier)
        data.update(new_data)
        # print(len(new_data))
        if len(new_data) >= size:
            break


if __name__ == "__main__":
    metadata = prep()
    print(f"Init: {len(metadata.link_data)} Pages expanded")
    while True:
        expand(metadata.queue, metadata.link_data, metadata.visited, 20)
        # print("NEW", frontier)
        post(metadata)
        print(f"WRITE: {len(metadata.link_data)} Pages expanded")
