import os
import importlib
from copy import deepcopy


def test():
    with open(f"output.log", "w") as log:
        try:
            from correction import FibonacciHeap
        except Exception as e:
            log.write(f"Error : {e}")

        try:
            heap = FibonacciHeap()
        except NameError as e:
            log.write(f"Error : Creation of the heap failed\n")
        else:
            log.write("Create heap successful\n")

        try:
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
        except Exception as e:
            log.write(f"Error while inserting good values in the heap: {e}\n")
        else:
            log.write(f"Insert successful\n")

        try:
            minimum = heap.find_min()
        except Exception as e:
            log.write(
                f"Error while finding minimum with good values inserted in the heap : {e}\n")
            return
        else:
            if minimum != 0:
                log.write(
                    f"Invalid : Found minimum {minimum} but was looking for 0\n")
            else:
                log.write(f"Find minimum successful\n")

        try:
            heap2 = deepcopy(heap)
            heap.merge(heap2)
        except Exception as e:
            log.write(f"Error while merging two identical heap : {e}\n")
        else:
            minimum = heap.find_min()
            if minimum != 0:
                log.write(
                    f"Invalid : Found minimum {minimum} but was looking for 0 after merge\n")
            else:
                log.write(f"Merge minimum successful\n")

        try:
            node = heap.delete_min()
        except Exception as e:
            log.write(f"Error while removing min element : {e}\n")
            return
        else:
            if node == 0:
                log.write("Delete minimum successful\n")
            else:
                log.write(
                    f"Error while removing minimum : Expected 0 got {node}")
                return

        try:
            while (node := heap.delete_min()) is not None:
                pass
        except Exception as e:
            log.write(f"Error while removing all elements : {e}\n")
        else:
            log.write(f"Delete minimum successful\n")
test()
