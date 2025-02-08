import json
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from utils import SchedulingEstimation, IterativeJump  # Import Pydantic models

# Load estimation data
estimation_path = Path("data/estimation.json")
with estimation_path.open() as f:
    estimation_data = json.load(f)

# Parse data using the SchedulingEstimation model
scheduling_estimation = SchedulingEstimation(**estimation_data)

# Extract iterative_adjust_jump data
iterative_jumps = scheduling_estimation.iterative_adjust_jump

# Prepare data for plotting
iterations = list(range(1, len(iterative_jumps) + 1))
rand_jumps = [jump.rand_cross_node_jump for jump in iterative_jumps]
brute_force_jumps = [jump.brute_force_cross_node_jump for jump in iterative_jumps]
it_jumps = [jump.it_cross_node_jump for jump in iterative_jumps]

# Plotting cross-node jumps
plt.figure(figsize=(10, 6))
plt.plot(iterations, rand_jumps, label='Random Scheduler Jumps')
plt.plot(iterations, brute_force_jumps, label='Brute-force Scheduler Jumps')
plt.plot(iterations, it_jumps, label='Iterative Scheduler Jumps')

# Add labels and legend
plt.xlabel('Batch (100 Walker Runs/Batch)')
plt.ylabel('Cross-Node Jumps')
plt.title('Trends of Cross-Node Jumps Over Iterations')
plt.legend()
plt.grid(True)

# Ensure x-axis shows only integer values
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Show plot
plt.show()

# Plotting trend of moved pages
moved_pages_count = [len(jump.moved_pages) for jump in iterative_jumps]

plt.figure(figsize=(10, 6))
plt.plot(iterations, moved_pages_count, label='Moved Pages Trend', marker='o')

# Add labels and legend
plt.xlabel('Batch (100 Walker Runs/Batch)')
plt.ylabel('Number of Moved Pages')
plt.title('Trend of Moved Pages Over Iterations')
plt.legend()
plt.grid(True)

# Ensure x-axis shows only integer values
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

# Show plot
plt.show()
