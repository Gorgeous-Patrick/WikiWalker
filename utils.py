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


class IterativeJump(BaseModel):
    moved_pages: list[str]
    sched: list[list[str]]


class SchedulingEstimation(BaseModel):
    paths: list[list[str]]
    walker_count: int = 0
    avg_page_size: float = 0
    total_jump_count: int = 0
    rand_sched: list[list[str]] = []
    brute_force_sched: list[list[str]] = []
    greedy_best_sched: list[list[str]] = []
    iterative_adjust_jump: list[IterativeJump] = []

data_path = Path("data")
cache_path = data_path / "cache"
run_path = data_path / "run"
estimation_path = data_path / "estimation.json"
metadata_path = Path("data", "metadata.json")
network_path = Path("data", "network.json")
pagerank_path = Path("data", "pagerank.json")

NUM_NODES = 16
PAGES_PER_NODE = 3000

