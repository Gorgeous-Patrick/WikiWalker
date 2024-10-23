import json
from utils import Metadata, metadata_path, pagerank_path


def pre():
    with open(
        metadata_path, "r"
    ) as metadata_file:
        return Metadata.model_validate(json.load(metadata_file))
