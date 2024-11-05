import subprocess
import os
import json
import random
from fetch import fetch_and_save


class PIMNode:
    def __init__(self):
        self.scheduled_pages: set[str] = set()

    def __repr__(self):
        pages = ", ".join(self.scheduled_pages)
        return f"PIMNode({pages})"


NUM_NODES = 20
PAGES_PER_NODE = 3


# Calculate the avg of page text size
def avg_page_size(paths: list[list[str]]):
    total_size = 0
    page_list = []
    for path in paths:
        for page in path:
            if page not in page_list:
                page_list.append(page)
    for page in page_list:
        page_content = fetch_and_save(page).text
        total_size += len(page_content)
    return total_size / len(page_list)


def rand_sched(paths: list[list[str]]):
    pages = []
    for path in paths:
        for page in path:
            if page not in pages:
                pages.append(page)
    nodes = []
    for i in range(NUM_NODES):
        nodes.append(PIMNode())
    for page in pages:
        node_chosen = random.choice(
            [node for node in nodes if len(node.scheduled_pages) < PAGES_PER_NODE]
        )
        node_chosen.scheduled_pages.add(page)
    return nodes


def count_edge(paths: list[list[str]]):
    count = {}
    for path in paths:
        for i in range(len(path) - 1):
            edge = (min(path[i], path[i + 1]), max(path[i], path[i + 1]))
            edge_count = count.get(edge, 0)
            count[edge] = edge_count + 1

    return count


def sorted_best(paths: list[list[str]]):
    # Get the edge counts using count_edge function
    edge_counts = count_edge(paths)

    # Sort edges by frequency (descending order)
    sorted_edges = sorted(edge_counts.items(), key=lambda x: -x[1])

    # Track the allocation of pages to PIM nodes
    pim_nodes = []
    page_to_pim = {}

    # Allocate pages to PIM nodes
    for edge, _ in sorted_edges:
        page1, page2 = edge

        # Check if page1 is already assigned
        if page1 not in page_to_pim:
            assigned = False
            for pim_node in pim_nodes:
                if len(pim_node.scheduled_pages) < PAGES_PER_NODE:
                    pim_node.scheduled_pages.add(page1)
                    page_to_pim[page1] = pim_node
                    assigned = True
                    break
            if not assigned:
                new_pim_node = PIMNode()
                new_pim_node.scheduled_pages.add(page1)
                pim_nodes.append(new_pim_node)
                page_to_pim[page1] = new_pim_node

        # Check if page2 is already assigned
        if page2 not in page_to_pim:
            assigned = False
            for pim_node in pim_nodes:
                if len(pim_node.scheduled_pages) < PAGES_PER_NODE:
                    pim_node.scheduled_pages.add(page2)
                    page_to_pim[page2] = pim_node
                    assigned = True
                    break
            if not assigned:
                new_pim_node = PIMNode()
                new_pim_node.scheduled_pages.add(page2)
                pim_nodes.append(new_pim_node)
                page_to_pim[page2] = new_pim_node

    return pim_nodes


# A brute force scheduler algorithm. Start with a random scheduling and try all possible permutations of the scheduling.
def brute_force_random(paths: list[list[str]]):
    pages = []
    for path in paths:
        for page in path:
            if page not in pages:
                pages.append(page)
    nodes = []
    for i in range(NUM_NODES):
        nodes.append(PIMNode())
    for page in pages:
        node_chosen = random.choice(
            [node for node in nodes if len(node.scheduled_pages) < PAGES_PER_NODE]
        )
        node_chosen.scheduled_pages.add(page)
    best_cross_node_jump = 0
    best_total_jump = 0
    best_sched = nodes
    for i in range(100000):
        new_nodes = []
        for i in range(NUM_NODES):
            new_nodes.append(PIMNode())
        for page in pages:
            node_chosen = random.choice(
                [
                    node
                    for node in new_nodes
                    if len(node.scheduled_pages) < PAGES_PER_NODE
                ]
            )
            node_chosen.scheduled_pages.add(page)
        cross_node_jump, total_jump = estimate_sched(paths, new_nodes)
        if cross_node_jump < best_cross_node_jump:
            best_cross_node_jump = cross_node_jump
            best_total_jump = total_jump
            best_sched = new_nodes
    return best_sched


# Greedy algorithm that tries to minimize the number of cross-node jumps. You start by random scheduling and then try to move pages to other nodes to reduce the number of cross-node jumps.
def greedy_best(paths: list[list[str]]):
    pages = []
    for path in paths:
        for page in path:
            if page not in pages:
                pages.append(page)
    nodes = []
    for i in range(NUM_NODES):
        nodes.append(PIMNode())
    for page in pages:
        node_chosen = random.choice(
            [node for node in nodes if len(node.scheduled_pages) < PAGES_PER_NODE]
        )
        node_chosen.scheduled_pages.add(page)
    best_cross_node_jump, best_total_jump = estimate_sched(paths, nodes)
    best_sched = nodes
    for i in range(100000):
        new_nodes = []
        for i in range(NUM_NODES):
            new_nodes.append(PIMNode())
        for page in pages:
            node_chosen = random.choice(
                [
                    node
                    for node in new_nodes
                    if len(node.scheduled_pages) < PAGES_PER_NODE
                ]
            )
            node_chosen.scheduled_pages.add(page)
        cross_node_jump, total_jump = estimate_sched(paths, new_nodes)
        if cross_node_jump < best_cross_node_jump:
            best_cross_node_jump = cross_node_jump
            best_total_jump = total_jump
            best_sched = new_nodes
    return best_sched


# A scheduler that takes the current scheduling and the paths that walkers took (accumulated) and adjusts the scheduling to minimize the number of cross-node jumps.
def adjust_sched(paths: list[list[str]], sched: list[PIMNode]):
    cross_node_jump, total_jump = estimate_sched(paths, sched)
    pages = []
    for path in paths:
        for page in path:
            if page not in pages:
                pages.append(page)
    best_cross_node_jump, best_total_jump = estimate_sched(paths, sched)
    best_sched = sched
    for i in range(100000):
        new_nodes = []
        for i in range(NUM_NODES):
            new_nodes.append(PIMNode())
        for page in pages:
            node_chosen = random.choice(
                [
                    node
                    for node in new_nodes
                    if len(node.scheduled_pages) < PAGES_PER_NODE
                ]
            )
            node_chosen.scheduled_pages.add(page)
        cross_node_jump, total_jump = estimate_sched(paths, new_nodes)
        if cross_node_jump < best_cross_node_jump:
            best_cross_node_jump = cross_node_jump
            best_total_jump = total_jump
            best_sched = new_nodes
    return best_sched


def estimate_sched(paths: list[list[str]], sched: list[PIMNode]):
    cross_node_jump = 0
    total_jump = 0
    location = {}
    for idx, node in enumerate(sched):
        for page in node.scheduled_pages:
            location[page] = idx
    for path in paths:
        cur_location = -1
        for page in path:
            new_page_location = location[page]
            if cur_location != -1:
                if cur_location != new_page_location:
                    cross_node_jump += 1
                total_jump += 1
            cur_location = new_page_location
    return cross_node_jump, total_jump


# for i in range(10):
#   new_env = os.environ.copy()
#   new_env["SEED"] = str(i)
#   subprocess.run(["jac", "run", "wikiwalker.jac"], env=new_env)
#   result = []
#   with open("single_result.json", "r") as f:
#     result.append(json.load(f))
#   print(result)

random.seed(0)
with open("result.json", "r") as result_file:
    paths = json.load(result_file)
    # print(rand_sched(result))
    print(avg_page_size(paths))
    print(estimate_sched(paths, rand_sched(paths)))
    print(estimate_sched(paths, sorted_best(paths)))
    print(estimate_sched(paths, brute_force_random(paths)))
    print(estimate_sched(paths, greedy_best(paths)))

    print("Iterate")
    sched = rand_sched(paths)
    for i in range(1, 1000):
        sched = adjust_sched(paths * i, sched)
        jump, total = estimate_sched(paths * i, sched)
        print(jump / total)
