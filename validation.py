import os
import importlib
from copy import deepcopy


def test(line):
    repository_url = line.split(",")[-1]
    repository_name = repository_url.split("/")[-1].strip("\n")

    os.chdir(f"{base_dir}\\repositories")
    os.system(f"git clone {repository_url} -q")
    os.system(f"cd {repository_name} && git pull")

base_dir = os.getcwd()
with open("urls.csv", "r") as f:
    f.readline()
    coroutines = []
    while line := f.readline():
        test(line)
