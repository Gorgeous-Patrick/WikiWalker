import subprocess
import os
import json


result = []
for i in range(50):
    new_env = os.environ.copy()
    new_env["SEED"] = str(i)
    subprocess.run(["jac", "run", "wikiwalker.jac"], env=new_env)
    with open("single_result.json", "r") as f:
        result.append(json.load(f))

with open("result.json", "w") as f:
    json.dump(result, f)
