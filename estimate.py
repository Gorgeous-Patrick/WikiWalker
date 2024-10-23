import subprocess
import os
import json
import random


class PIMNode:
    def __init__(self):
        self.scheduled_pages: set[str] = set()

    def __repr__(self):
        pages = ", ".join(self.scheduled_pages)
        return f"PIMNode({pages})"


NUM_NODES = 20
PAGES_PER_NODE = 3


def rand_sched(paths: list[list[str]]):
    pages = set()
    for path in paths:
        for page in path:
            pages.add(page)
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
            edge = (path[i], path[i + 1])
            edge_count = count.get(edge, 0)
            count[edge] = edge_count + 1

            edge = (path[i + 1], path[i])
            count[edge] = edge_count + 1
    return count


def greedy_best(paths: list[list[str]]):
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
    print(estimate_sched(paths, rand_sched(paths)))
    print(estimate_sched(paths, greedy_best(paths)))
