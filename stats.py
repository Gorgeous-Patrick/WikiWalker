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


def get_total_transfer_time_per_jump(IJ: IterativeJump):
    return (
        IJ.total_jump_this_iter * WALKER_SIZE / IN_PE_SPEED
        + IJ.cross_node_jump * WALKER_SIZE / PE_TO_HOST_SPEED
        + len(IJ.moved_pages) * PAGE_SIZE / PE_TO_HOST_SPEED
    )


estimation = get_estimation()
print("RAND", get_total_transfer_time(estimation.total_jump_count, estimation.rand_sched_jump))
print("GREEDY", get_total_transfer_time(estimation.total_jump_count, estimation.greedy_best_jump))

print("Iterative Jump")
for IJ in estimation.iterative_adjust_jump:
    print(get_total_transfer_time_per_jump(IJ))

# Sum of all the transfer time
total_transfer_time = sum(
    get_total_transfer_time_per_jump(IJ) for IJ in estimation.iterative_adjust_jump
)
print("Total Transfer Time")
print(total_transfer_time)

# Plotting the transfer time as a line plot with dash line
plt.plot(
    [get_total_transfer_time_per_jump(IJ) for IJ in estimation.iterative_adjust_jump],
    linestyle="--",
    label="Transfer Time per Jump",
)

plt.show()