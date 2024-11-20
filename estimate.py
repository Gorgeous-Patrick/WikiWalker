import json
import random
from utils import run_path, SchedulingEstimation, estimation_path, IterativeJump, PageInfo, NUM_NODES, PAGES_PER_NODE
import copy


def read_page_text(title: str):
    with open(f"data/cache/{title.replace('/', '_')}.json", "r") as file:

        parsed = json.load(file)
        page = PageInfo(**parsed)
        return page.text


def save_result(result: SchedulingEstimation):
    with open(estimation_path, "w") as f:
        f.write(result.model_dump_json())


# Calculate the avg of page text size
def avg_page_size(paths: list[list[str]]):
    total_size = 0
    page_list = []
    for path in paths:
        for page in path:
            if page not in page_list:
                page_list.append(page)
    for page in page_list:
        page_content = read_page_text(page)
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
        nodes.append([])
    for page in pages:
        node_chosen = random.choice(
            [node for node in nodes if len(node) < PAGES_PER_NODE]
        )
        node_chosen.append(page)
    return nodes


def count_edge(paths: list[list[str]]):
    count = {}
    for path in paths:
        for i in range(len(path) - 1):
            edge = (min(path[i], path[i + 1]), max(path[i], path[i + 1]))
            edge_count = count.get(edge, 0)
            count[edge] = edge_count + 1

    return count


# A brute force scheduler algorithm. Start with a random scheduling and try all possible permutations of the scheduling.
def brute_force_random(paths: list[list[str]]):
    pages = []
    for path in paths:
        for page in path:
            if page not in pages:
                pages.append(page)
    nodes = []
    for i in range(NUM_NODES):
        nodes.append([])
    for page in pages:
        node_chosen = random.choice(
            [node for node in nodes if len(node) < PAGES_PER_NODE]
        )
        node_chosen.append(page)
    best_cross_node_jump = float("inf")
    best_sched = nodes
    for i in range(10000):
        print(i)
        new_nodes = []
        for i in range(NUM_NODES):
            new_nodes.append([])
        for page in pages:
            node_chosen = random.choice(
                [
                    node
                    for node in new_nodes
                    if len(node) < PAGES_PER_NODE
                ]
            )
            node_chosen.append(page)
        cross_node_jump = estimate_sched(paths, new_nodes)
        if cross_node_jump < best_cross_node_jump:
            best_cross_node_jump = cross_node_jump
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
        nodes.append([])
    for page in pages:
        node_chosen = random.choice(
            [node for node in nodes if len(node) < PAGES_PER_NODE]
        )
        node_chosen.append(page)
    best_cross_node_jump = estimate_sched(paths, nodes)
    best_sched = nodes
    # Every time we swap two pages, we check if the number of cross-node jumps is reduced.
    for i in range(20000):
        # Randomly choose two different pages
        page1 = random.choice(pages)
        page2 = random.choice(pages)
        while page1 == page2:
            page2 = random.choice(pages)

        # Find the nodes that contain the two pages
        node1 = None
        node2 = None
        for node in nodes:
            if page1 in node:
                node1 = node
            if page2 in node:
                node2 = node
        # Swap the two pages
        node1.remove(page1)
        node2.remove(page2)
        node1.append(page2)
        node2.append(page1)
        # Check if the number of cross-node jumps is reduced
        cross_node_jump = estimate_sched(paths, nodes)
        if cross_node_jump < best_cross_node_jump:
            best_cross_node_jump = cross_node_jump
            best_sched = nodes
        else:
            # If not, swap back
            node1.remove(page2)
            node2.remove(page1)
            node1.append(page1)
            node2.append(page2)
        print(i, cross_node_jump)
    return best_sched


# A scheduler that takes the current scheduling and the paths that walkers took (accumulated) and adjusts the scheduling to minimize the number of cross-node jumps.
def adjust_sched(paths: list[list[str]], sched: list[list[str]]):
    cross_node_jump = estimate_sched(paths, sched)
    best_cross_node_jump = cross_node_jump
    pages = []
    for path in paths:
        for page in path:
            if page not in pages:
                pages.append(page)
    nodes = sched
    best_sched = sched
    # Every time we swap two pages, we check if the number of cross-node jumps is reduced.
    for i in range(100):
        # Randomly choose two different pages
        page1 = random.choice(pages)
        page2 = random.choice(pages)
        while page1 == page2:
            page2 = random.choice(pages)

        # Find the nodes that contain the two pages
        node1 = None
        node2 = None
        for node in nodes:
            if page1 in node:
                node1 = node
            if page2 in node:
                node2 = node
        # Swap the two pages
        node1.remove(page1)
        node2.remove(page2)
        node1.append(page2)
        node2.append(page1)
        # Check if the number of cross-node jumps is reduced
        cross_node_jump = estimate_sched(paths, nodes)
        if cross_node_jump < best_cross_node_jump:
            best_cross_node_jump = cross_node_jump
            best_sched = nodes
        else:
            # If not, swap back
            node1.remove(page2)
            node2.remove(page1)
            node1.append(page1)
            node2.append(page2)
    return best_sched


def total_jump(paths: list[list[str]]):
    total_jump = 0
    for path in paths:
        total_jump += len(path) - 1
    return total_jump


def estimate_sched(paths: list[list[str]], sched: list[list[str]]):
    cross_node_jump = 0
    location = {}
    for idx, node in enumerate(sched):
        for page in node:
            location[page] = idx
    for path in paths:
        cur_location = -1
        for page in path:
            new_page_location = location[page]
            if cur_location != -1:
                if cur_location != new_page_location:
                    cross_node_jump += 1
            cur_location = new_page_location
    return cross_node_jump


def compare_schedules(sched: list[list[str]], new_sched: list[list[str]]):
    moved_pages = []
    location = {}
    for idx, node in enumerate(sched):
        for page in node:
            location[page] = idx
    new_location = {}
    for idx, node in enumerate(new_sched):
        for page in node:
            new_location[page] = idx
    for page, loc in location.items():
        if loc != new_location[page]:
            moved_pages.append(page)
    return moved_pages

if __name__ == "__main__":
    random.seed(0)
    paths = []
    # Read all paths
    for file_name in run_path.iterdir():
        with open(file_name, "r") as file:
            path = json.load(file)
            paths.append(path)
        # print(rand_sched(result))
    print(avg_page_size(paths))
    result = SchedulingEstimation(paths=paths, avg_page_size=avg_page_size(paths))
    result.rand_sched = rand_sched(paths)
    save_result(result)
    result.brute_force_sched = brute_force_random(paths)
    save_result(result)
    result.greedy_best_sched = greedy_best(paths)
    save_result(result)
    # result.iterative_adjust_jump = []
    # print(estimate_sched(paths, rand_sched(paths)))
    # print(estimate_sched(paths, sorted_best(paths)))
    # print(estimate_sched(paths, brute_force_random(paths)))
    # print(estimate_sched(paths, greedy_best(paths)))

    print("Iterate")
    print("Number of walkers:", len(paths))
    step = 100
    sched = rand_sched(paths)
    for i in range(step, len(paths), step):
        new_sched = adjust_sched(paths[:i], copy.deepcopy(sched))
        moved_pages = compare_schedules(sched, new_sched)
        print("Moved pages:", len(moved_pages))
        # if len(moved_pages) > 0:
        #     print("Moved pages:", moved_pages)
        #     break
        sched = new_sched
        total = total_jump(paths[(i - step) : i])
        jump = estimate_sched(paths[(i - step) : i], sched)
        result.iterative_adjust_jump.append(
            IterativeJump(
                moved_pages=moved_pages, cross_node_jump=jump, sched=sched
            )
        )
        save_result(result)
        print(jump / total)
    # Remind to talk about twitter app..
