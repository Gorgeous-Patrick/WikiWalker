from pydantic import BaseModel
from pathlib import Path


class Metadata(BaseModel):
    link_data: dict[str, list[str]] = {}
    visited: list[str] = []
    queue: list[str] = []


data_path = Path("data")
metadata_path = Path("data", "metadata.json")
pagerank_path = Path("data", "pagerank.json")
