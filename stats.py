from utils import SchedulingEstimation, estimation_path, IterativeJump
import json
import matplotlib.pyplot as plt


def get_estimation():
    with open(estimation_path, "r") as f:
        return SchedulingEstimation(**json.load(f))


# Internal speed is 128 GB / s
IN_PE_SPEED = 128 * 1024 * 1024 * 1024

# PE to Host speed is 19.2 GB / s
PE_TO_HOST_SPEED = 19.2 * 1024 * 1024 * 1024

# Walker size
WALKER_SIZE = 3000

# Page size
PAGE_SIZE = 7000


def get_total_transfer_time(total_jump_count: int, cross_node_jump: int):
    print(total_jump_count, cross_node_jump)
    return (
        total_jump_count * WALKER_SIZE / IN_PE_SPEED
        + cross_node_jump * WALKER_SIZE / PE_TO_HOST_SPEED * 2
    )


def in_pe_transfer_time(IJ: IterativeJump):
    return (IJ.total_jump_this_iter - IJ.cross_node_jump) * WALKER_SIZE / IN_PE_SPEED

def cross_node_transfer_time(IJ: IterativeJump):
    return IJ.cross_node_jump * WALKER_SIZE / PE_TO_HOST_SPEED

def page_transfer_time(IJ: IterativeJump):
    return len(IJ.moved_pages) * PAGE_SIZE / PE_TO_HOST_SPEED


def get_total_transfer_time_per_jump(IJ: IterativeJump):
    return (
        (IJ.total_jump_this_iter - IJ.cross_node_jump) * WALKER_SIZE / IN_PE_SPEED
        + IJ.cross_node_jump * WALKER_SIZE / PE_TO_HOST_SPEED
        + len(IJ.moved_pages) * PAGE_SIZE / PE_TO_HOST_SPEED
    )


estimation = get_estimation()
print(
    "RAND",
    get_total_transfer_time(estimation.total_jump_count, estimation.rand_sched_jump),
)
print(
    "GREEDY",
    get_total_transfer_time(estimation.total_jump_count, estimation.greedy_best_jump),
)

print("Iterative Jump")
for IJ in estimation.iterative_adjust_jump:
    print(get_total_transfer_time_per_jump(IJ))

# Sum of all the transfer time
total_transfer_time = sum(
    get_total_transfer_time_per_jump(IJ) for IJ in estimation.iterative_adjust_jump
)
print("Total Transfer Time")
print(total_transfer_time)

# Plotting the transfer time as a line plot with dash line, x axis is the iteration, y axis is the transfer time

plt.plot(
    [get_total_transfer_time_per_jump(IJ) for IJ in estimation.iterative_adjust_jump],
    linestyle="-",
    label="Iterative Scheduler",
)
# X axis is the iteration
plt.xlabel("Iteration")
# Y axis is the transfer time
plt.ylabel("Transfer Time (s)")
# X axis only has integer values
plt.xticks(range(len(estimation.iterative_adjust_jump)))

# Also show random and greedy transfer time (divide by iteration length)
plt.axhline(
    y=get_total_transfer_time(estimation.total_jump_count, estimation.rand_sched_jump)
    / len(estimation.iterative_adjust_jump),
    color="r",
    linestyle="--",
    label="Random Transfer Time",
)
plt.axhline(
    y=get_total_transfer_time(estimation.total_jump_count, estimation.greedy_best_jump)
    / len(estimation.iterative_adjust_jump),
    color="g",
    linestyle="--",
    label="Greedy Transfer Time",
)

# Add a title
plt.title("21095 Pages, 1851 Walker runs")

plt.legend()
plt.show()

# Make another plot. For each iteration, bar plot the 3 different transfer time with different color

plt.bar(
    range(len(estimation.iterative_adjust_jump)),
    [in_pe_transfer_time(IJ) for IJ in estimation.iterative_adjust_jump],
    color="r",
    label="In PE Transfer Time",
)
plt.bar(
    range(len(estimation.iterative_adjust_jump)),
    [cross_node_transfer_time(IJ) for IJ in estimation.iterative_adjust_jump],
    color="g",
    label="Cross Node Transfer Time",
    bottom=[in_pe_transfer_time(IJ) for IJ in estimation.iterative_adjust_jump],
)
plt.bar(
    range(len(estimation.iterative_adjust_jump)),
    [page_transfer_time(IJ) for IJ in estimation.iterative_adjust_jump],
    color="b",
    label="Page Transfer Time",
    bottom=[
        in_pe_transfer_time(IJ) + cross_node_transfer_time(IJ)
        for IJ in estimation.iterative_adjust_jump
    ],
)
plt.xlabel("Iteration")
plt.ylabel("Transfer Time (s)")
plt.xticks(range(len(estimation.iterative_adjust_jump)))
plt.title("21095 Pages, 1851 Walker runs")
plt.legend()
plt.show()

