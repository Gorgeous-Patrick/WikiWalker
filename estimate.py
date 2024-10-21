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

def evaluate_sche():
  pass
  

  


# for i in range(10):
#   new_env = os.environ.copy()
#   new_env["SEED"] = str(i)
#   subprocess.run(["jac", "run", "wikiwalker.jac"], env=new_env)
#   result = []
#   with open("single_result.json", "r") as f:
#     result.append(json.load(f))
#   print(result)

print(rand_sched(["ABA", 'BAB', "CAC"]))


  
    
