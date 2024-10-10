import json
from utils import Metadata, metadata_path, pagerank_path


def pre():
    with open(pagerank_path, "r") as pagerank_file, open(
        metadata_path, "r"
    ) as metadata_file:
        return Metadata.model_validate(json.load(metadata_file)), json.load(
            pagerank_file
        )


def next(name: str, metadata: Metadata, pagerank: dict[str, float]):
    potential = [
        next_name
        for next_name in metadata.link_data[name]
        if next_name in pagerank.keys()
    ]
    max_rank = 0.0
    max_page_name = None
    for next_name in potential:
        if max_rank < pagerank[next_name]:
            max_rank = pagerank[next_name]
            max_page_name = next_name
    # print(max_rank)

    return max_page_name


def walk(name: str, iterations: int, metadata: Metadata, pagerank: dict[str, float]):
    cur = name
    result = [cur]
    for _ in range(iterations):
        cur = next(cur, metadata, pagerank)
        if cur is None:
            return result
        result.append(cur)


def spawn(
    walker_num: int, iterations: int, metadata: Metadata, pagerank: dict[str, float]
):
    name_list = list(pagerank.keys())
    assert walker_num <= len(name_list)
    for name in name_list:
        path = walk(name, iterations, metadata, pagerank)
        if path is not None and len(path) >= 2:
            print(path)


if __name__ == "__main__":
    metadata, pagerank = pre()
    print(len(pagerank))
    spawn(1, 10, metadata, pagerank)
