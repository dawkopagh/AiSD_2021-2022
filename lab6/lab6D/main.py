# This is a version of https://gist.github.com/natekupp/1763661 without
# using mutation and with some other simplifications. Hopefully it's slightly
# easier to follow. Performance wise - from some small benchmarking - it has
# the same O(N) characteristics/memory usage, but is about twice as slow.
#
# Use it like:
#
#    b = Node([], [])
#    b = add(b, n)
#    print(pp(b))
#    print(search(b, x))
#
from __future__ import annotations
from dataclasses import dataclass

MAX_KEYS = 5  # must be odd
J = MAX_KEYS // 2  # the index of the middle element

@dataclass
class Node:
    keys: list[int]
    children: list[Node]

def add(node: Node, k: int) -> Node:
    if len(node.keys) == MAX_KEYS:
        node = _split(Node([], [node]), 0)
    return _insert(node, k)

def _insert(node: Node, k: int) -> Node:
    i = next((i for i, key in enumerate(node.keys) if k < key), len(node.keys))

    if not node.children:  # i.e. is a leaf
        return Node(node.keys[:i] + [k] + node.keys[i:], node.children)

    if len(node.children[i].keys) ==  MAX_KEYS:
        node = _split(node, i)
        i = i + 1 if k > node.keys[i] else i

    new_child = _insert(node.children[i], k)
    return Node(node.keys, node.children[:i] + [new_child] + node.children[i+1:])

def _split(node: Node, i: int) -> Node:
    child = node.children[i]
    keys_before, key, keys_after = child.keys[:J], child.keys[J], child.keys[J + 1:]
    children_before, children_after = child.children[:J + 1], child.children[J + 1:]

    return Node(
        node.keys[:i] + [key] + node.keys[i:],
        node.children[:i] + [
            Node(keys_before, children_before),
            Node(keys_after, children_after),
        ] + node.children[i + 1:],
    )

def search(node: Node, k: int) -> bool:
    if not node.children:
        return k in node.keys

    return next(
        True if k == key else search(child, k)
        for key, child in zip(node.keys + [10 ** 10], node.children)
        if k <= key
    )

def pp(node: Node, indent: int = 0) -> str:
    return "\n".join("  " * indent + line for line in [
        f"keys: {node.keys} {'children:' if node.children else ''}",
        *[f"  {pp(child, indent + 1)}" for child in node.children],
    ])


B = Node([],[])
for inx in range(10):
    B.add((inx,inx))