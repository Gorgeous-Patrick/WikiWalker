from pydantic import BaseModel
from pathlib import Path

class PageInfo(BaseModel):
    title: str
    text: str
    links: list[str]
    images: list[str]

class Network(BaseModel):
    nodes: list[str]
    links: dict[str, list[str]]


data_path = Path("data")
cache_path = data_path / "cache"
run_path = data_path / "run"
metadata_path = Path("data", "metadata.json")
network_path = Path("data", "network.json")
pagerank_path = Path("data", "pagerank.json")
