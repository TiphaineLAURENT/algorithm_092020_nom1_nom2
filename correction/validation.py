import os
import importlib

def test_heap(heap):
    heap.insert(5)
    heap.insert(1)
    heap.insert(10)
    heap.insert(0)
    heap.insert(42)
    heap.insert(15)
    heap.insert(7)
    heap.insert(19)
    heap.insert(20)
    heap.insert(2)
    heap.insert(84)
    heap.insert(50)

    while (node := heap.delete_min()) is not None:
        print(node)

base_dir = os.getcwd()
with open("urls.csv", "r") as f:
    f.readline()
    coroutines = []
    while line := f.readline():
        repository_url = line.split(",")[-1]
        repository_name = repository_url.split("/")[-1].strip("\n")

        with open(f"{repository_name}.log", "w") as log:
            os.chdir(f"{base_dir}\\repositories")
            os.system(f"git clone {repository_url} -q && cd {repository_name} && git pull")

            os.chdir(f"{base_dir}\\logs")
            try:
                module = importlib.import_module(f"{repository_name}.fibonacci_heap")
            except ModuleNotFoundError as e:
                log.write(f"{e}\n")

            try:
                heap = module.FibonacciHeap()
                test_heap(heap)
            except Exception as e:
                log.write(f"{e}\n")
