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
    rand_cross_node_jump: int
    brute_force_cross_node_jump: int
    it_cross_node_jump: int
    total_jump_this_iter: int


class SchedulingEstimation(BaseModel):
    paths: list[list[str]]
    walker_count: int = 0
    avg_page_size: float = 0
    total_jump_count: int = 0
    # rand_sched_jump: int = 0
    # brute_force_rand_jump: int = 0
    # greedy_best_jump: int = 0
    iterative_adjust_jump: list[IterativeJump] = []


data_path = Path("data")
cache_path = data_path / "cache"
run_path = data_path / "run"
estimation_path = data_path / "estimation.json"
metadata_path = Path("data", "metadata.json")
network_path = Path("data", "network.json")
pagerank_path = Path("data", "pagerank.json")
