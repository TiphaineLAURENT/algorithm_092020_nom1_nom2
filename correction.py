class Node(object):
    def __init__(self, key: int, parent: object = None, left: object = None, right: object = None,
                 child: object = None, mark: bool = False):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent
        self.child = child  # to any one of its children
        self.degree = 0
        self.mark = mark

    def add_child(self, child: object) -> None:
        if not self.child:
            self.child = child
            child.left, child.right = child, child
        else:
            right_to_child = self.child.right
            self.child.right = child
            child.left = self.child
            child.right = right_to_child
            right_to_child.left = child
        child.parent = self
        self.degree += 1
        child.mark = False

    def remove_child(self, child: object) -> None:
        if not self.child:
            raise ValueError('Child list is currently empty')
        if self.degree == 1:
            self.child = None
        else:  # self.degree >= 2
            if self.child is child:
                self.child = child.right
            left_to_child, right_to_child = child.left, child.right
            left_to_child.right = right_to_child
            right_to_child.left = left_to_child
        self.degree -= 1


class FibonacciHeap(object):
    def __init__(self, minimum: Node = None):
        self.min = minimum
        self.num_nodes = 0
        self.num_trees = 0
        self.num_marks = 0

    def remove_root(self, root: Node) -> None:
        right_to_root, left_to_root = root.right, root.left
        right_to_root.left = left_to_root
        left_to_root.right = right_to_root
        self.num_trees -= 1

    def add_root(self, root: Node) -> None:
        if self.min == None:
            root.left, root.right = root, root
        else:
            right_to_min = self.min.right
            self.min.right = root
            root.left = self.min
            root.right = right_to_min
            right_to_min.left = root
        self.num_trees += 1

    def insert(self, value: int) -> None:
        node = Node(value)
        if self.min is None:
            self.add_root(node)
            self.min = node
        else:
            self.add_root(node)
            if node.key < self.min.key:
                self.min = node
        self.num_nodes += 1

    def find_min(self) -> Node:
        return self.min

    def delete_min(self) -> int:
        minimum = self.min
        if minimum is not None:
            minimum_child = minimum.child
            for i in range(minimum.degree):
                minimum_child_right_branch = minimum_child.right
                self.add_root(minimum_child)
                minimum_child.parent = None
                minimum_child = minimum_child_right_branch
            if minimum.mark:
                self.num_marks -= 1
            self.remove_root(minimum)
            if minimum == minimum.right:
                self.min = None
            else:
                self.min = minimum.right
                self.consolidate()
            self.num_nodes -= 1
            return minimum.key
        return minimum

    def consolidate(self) -> None:
        unsorted_nodes = [None] * self.num_nodes

        #[degree0, degree1, degree2...]

        root = self.min
        counter = self.num_trees
        while counter:
            temp_root = root
            root = root.right
            temp_root_degree = temp_root.degree
            while unsorted_nodes[temp_root_degree]: # Regarde est-ce qu'il existe une branche de la même taille
                node_with_similar_degree = unsorted_nodes[temp_root_degree]
                if temp_root.key > node_with_similar_degree.key: # Si la branche similaire a une valeur superieur, la branche similaire va en dessous
                    # Echanger les valeurs de a et b
                    # Pour a == 1 et b == 2
                    # temp = a == 1
                    # a = b == 2
                    # b = temp == 1
                    # a == 2 et b == 1
                    temp_root, node_with_similar_degree = node_with_similar_degree, temp_root
                self.link(node_with_similar_degree, temp_root)
                unsorted_nodes[temp_root_degree] = None # On enlève la branche similaire de la liste des branches similaire
                temp_root_degree += 1
            unsorted_nodes[temp_root_degree] = temp_root
            counter -= 1
        self.min = None
        for i in range(len(unsorted_nodes)):
            if unsorted_nodes[i]:
                if self.min is None:
                    self.min = unsorted_nodes[i]
                else:
                    if unsorted_nodes[i].key < self.min.key:
                        self.min = unsorted_nodes[i]

    def link(self, first: Node, second: Node) -> None:  # y > x
        self.remove_root(first)
        if first.mark:
            self.num_marks -= 1
        second.add_child(first)

    def merge(self, other: object) -> None:
        if not self.min:
            self.min = other.min
        elif other.min:
            self_first_root, other_last_root = self.min.right, other.min.left
            self_first_root.left = other_last_root
            self.min.right = other.min
            other.min.left = self.min
            other_last_root.right = self_first_root

        if self.min is None or (other.min is not None and other.min.key < self.min.key):
            self.min = other.min
        self.num_nodes += other.num_nodes
        self.num_trees += other.num_trees
        self.num_marks += other.num_marks

    def decrease_key(self, node: Node, new_key: int) -> None:
        if new_key > node.key:
            raise ValueError('new key is greater than current key')
        node.key = new_key
        y = node.p
        if y and node.key < y.key:
            self.cut(node, y)
            self.cascading_cut(y)
        if node.key < self.min.key:
            self.min = node

    def cut(self, node: Node, parent: Node) -> None:
        if node.mark:
            self.num_marks -= 1
            node.mark = False
        parent.remove_child(node)
        self.add_root(node)
        node.parent = None

    def cascading_cut(self, node: Node) -> None:
        if parent := node.parent and not node.mark:
            self.num_marks += 1
        else:
            self.cut(node, parent)
            self.cascading_cut(parent)

    def delete(self, node: Node) -> None:
        self.decrease_key(node, float("-inf"))
        self.delete_min()


heap = FibonacciHeap() # Create heap == 1

heap.insert(5) # Insert value == 1
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

print(heap.find_min()) # find min == 1

from copy import deepcopy

heap2 = deepcopy(heap)
heap.merge(heap2) # Fusion == 1

print(heap.find_min()) # Trouver le minimum fusionner

print(heap.delete_min()) # Prendre la valeur minimum == 3

while (node := heap.delete_min()) is not None: # Prendre jusqu'au dernier == gestion d'erreur
    print(node)
