from pathlib import Path
import json
from collections import defaultdict
import matplotlib.pyplot as plt
from utils import run_path, data_path

"""
This script analyzes walker transition probabilities based on JSON log files.

Purpose:
- Reads walker paths from 'run_path', where each JSON file represents a sequence of visited pages.
- Computes the probability of transitioning from one page to another.
- Extracts the top 'n' most probable transitions for each page.
- Computes the average probability for each rank (1st, 2nd, ..., nth most probable).
- Outputs the overall averages, providing insights into walker predictability.

Configurable Parameters:
- 'n': The number of ranked probabilities to compute.
"""

def compute_transition_probabilities(run_path: Path, n: int = 5):
    transition_counts = defaultdict(lambda: defaultdict(int))
    
    # Read all walker paths from run_path
    for json_file in run_path.glob("*.json"):
        with open(json_file, "r") as f:
            path = json.load(f)
        
        # Count transitions between pages
        for i in range(len(path) - 1):
            current_page, next_page = path[i], path[i + 1]
            transition_counts[current_page][next_page] += 1
    
    # Compute transition probabilities
    transition_probs = {}
    for page, next_pages in transition_counts.items():
        total_transitions = sum(next_pages.values())
        sorted_probs = sorted(
            ((next_page, count / total_transitions) for next_page, count in next_pages.items()),
            key=lambda x: x[1], reverse=True
        )
        transition_probs[page] = [p for _, p in sorted_probs]
    
    # Compute average probabilities for each rank (1st, 2nd, ..., nth most probable)
    avg_probs = [0] * n
    count_pages = 0
    for probs in transition_probs.values():
        count_pages += 1
        for rank in range(min(n, len(probs))):
            avg_probs[rank] += probs[rank]
    
    # Normalize by the number of pages
    if count_pages > 0:
        avg_probs = [p / count_pages for p in avg_probs]
    
    # Output results
    print("Average Transition Probabilities (by rank):")
    for i, avg_p in enumerate(avg_probs):
        print(f"P_{i+1} (Top {i+1} most probable transition): {avg_p:.4f}")
    
    # Plot results and save the figure
    plt.figure(figsize=(10, 5))
    plt.bar(range(1, n+1), avg_probs, tick_label=[f"P_{i+1}" for i in range(n)])
    plt.xlabel("Rank of Most Probable Transition")
    plt.ylabel("Average Probability")
    plt.title("Average Transition Probabilities by Rank")
    
    # Save the plot instead of showing it
    plot_path = data_path / "transition_probabilities.png"
    plt.savefig(plot_path)
    print(f"Plot saved to {plot_path}")

# Example usage
n = 5  # Configurable value for the number of ranked probabilities to compute
compute_transition_probabilities(run_path, n)

