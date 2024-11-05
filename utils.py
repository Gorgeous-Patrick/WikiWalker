from pydantic import BaseModel
from pathlib import Path

class PageInfo(BaseModel):
    title: str
    text: str
    links: list[str]
    images: list[str]


data_path = Path("data")
cache_path = data_path / "cache"
metadata_path = Path("data", "metadata.json")
pagerank_path = Path("data", "pagerank.json")
