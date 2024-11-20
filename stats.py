from utils import SchedulingEstimation, estimation_path, IterativeJump, run_path, cache_path
import json
import matplotlib.pyplot as plt
from estimate import estimate_sched


def get_estimation():
    with open(estimation_path, "r") as f:
        return SchedulingEstimation(**json.load(f))

# PE to Host speed is 19.2 GB / s
PE_TO_HOST_SPEED = 19.2 * 1024 * 1024 * 1024

# Walker size
WALKER_SIZE = 3000

# Page size
PAGE_SIZE = 7000

def cross_node_transfer(paths: list[list[str]], sched: list[list[str]]) -> float:
    return estimate_sched(paths, sched) * WALKER_SIZE


def estimate_transfer_time(paths: list[list[str]], sched: list[list[str]], moved: list[str]) -> float:
    cross_node_transfer = estimate_sched(paths, sched) * WALKER_SIZE 
    page_transfer = len(moved) * PAGE_SIZE
    return cross_node_transfer + page_transfer


estimation = get_estimation()
# Merge all paths into a single list


# Plotting the transfer time as a line plot with dash line, x axis is the iteration, y axis is the transfer time

step = 100
iterative = estimation.iterative_adjust_jump
plt.plot(
    [estimate_transfer_time(estimation.paths[idx * step: (idx + 1)* step], iterative[idx].sched, iterative[idx].moved_pages) for idx in range(len(iterative))],
    linestyle="-",
    label="Iterative Scheduler",
)
plt.plot(
    [estimate_transfer_time(estimation.paths[idx * step: (idx + 1)* step], estimation.rand_sched, []) for idx in range(len(iterative))],
    linestyle="-",
    label="Random Scheduler",
)
plt.plot(
    [estimate_transfer_time(estimation.paths[idx * step: (idx + 1)* step], estimation.greedy_best_sched, []) for idx in range(len(iterative))],
    linestyle="-",
    label="Greedy Scheduler",
)

# X axis is the iteration
plt.xlabel("Iteration (100 Pages / Iteration)")
# Y axis is the transfer time
plt.ylabel("Data Transmitted (Bytes)")
# X axis only has integer values
plt.xticks(range(len(estimation.iterative_adjust_jump)))


# Add a title
plt.title(f"{len(list(cache_path.iterdir()))} Pages, {len(list(run_path.iterdir()))} Walker runs")

plt.legend()
plt.show()
