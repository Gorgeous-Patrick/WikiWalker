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

NUM_NODES = 10
PAGES_PER_NODE = 3

def rand_sched(pages: list[str]):
  nodes = []
  for i in range(NUM_NODES):
    nodes.append(PIMNode())
  for page in pages:
    node_chosen = random.choice([node for node in nodes if len(node.scheduled_pages) < PAGES_PER_NODE])
    node_chosen.scheduled_pages.add(page)
  return nodes

def count_edge(paths: list[list[str]]):
  count = {}
  for path in paths:
    for i in range(len(path) - 1):
      edge = (path[i], path[i+1])
      edge_count = count.get(edge, 0)
      count[edge] = edge_count + 1

      edge = (path[i + 1], path[i])
      count[edge] = edge_count + 1
  return count

def greedy_best(paths: list[list[str]]):
  edge_counts = count_edge(paths)
  checked = set()
  while len(checked) != len(edge_counts):
    max_edge = None
    max_value = 0
    for edge, value in enumerate(edge_counts):
      if edge not in checked and max_value < value:
        max_edge = edge
        max_value = value

    


      
  

  


# for i in range(10):
#   new_env = os.environ.copy()
#   new_env["SEED"] = str(i)
#   subprocess.run(["jac", "run", "wikiwalker.jac"], env=new_env)
#   result = []
#   with open("single_result.json", "r") as f:
#     result.append(json.load(f))
#   print(result)

print(rand_sched(["ABA", 'BAB', "CAC"]))


  
    
