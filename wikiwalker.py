import json
from utils import Metadata, metadata_path, pagerank_path


def pre():
    with open(pagerank_path, "r") as pagerank_file, open(
        metadata_path, "r"
    ) as metadata_file:
        return Metadata.model_validate(json.load(metadata_file)), json.load(
            pagerank_file
        )
