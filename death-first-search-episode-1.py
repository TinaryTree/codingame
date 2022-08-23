import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# n: the total number of nodes in the level, including the gateways
# l: the number of links
# e: the number of exit gateways
n, l, e = [int(i) for i in input().split()]
edges = []
for i in range(l):
    # n1: N1 and N2 defines a link between these nodes
    n1, n2 = [int(j) for j in input().split()]
    edges.append((n1, n2))

for i in range(e):
    ei = int(input())  # the index of a gateway node


class node:
    def __init__(self, index):
        self.index = index
        self.distence = 9999999
        self.adj_edges = self.adj_edges()

    def adj_edges(self):
        return [_ if self.index in _ else None for _ in edges]


nodes = [node(i) for i in range(l)]
print(edges, file=sys.stderr, flush=True)
print(nodes, file=sys.stderr, flush=True)
# game loop
while True:
    # The index of the node on which the Bobnet agent is positioned this turn
    si = int(input())

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # Example: 0 1 are the indices of the nodes you wish to sever the link between
    print(f"0 1")
