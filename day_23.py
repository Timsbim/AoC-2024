print("Day 23")
EXAMPLE = False

file_name = f"2024/input/day_23{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    EDGES = tuple(tuple(line.rstrip().split("-")) for line in file)

nodes = {i: n for i, n in enumerate(sorted({n for e in EDGES for n in e}))}
numbers, graph = {n: i for i, n in nodes.items()}, {n: [] for n in nodes}
for n0, n1 in sorted((numbers[n0], numbers[n1]) for n0, n1 in EDGES):
    if n0 < n1:
        graph[n0].append(n1)
    else:
        graph[n1].append(n0)
num_nodes, neighbours = len(graph), {n: set(ns) for n, ns in graph.items()}
cliques = [(n0, n1) for n0 in graph for n1 in graph[n0]]
for length in range(3, num_nodes):
    cliques_new = []
    for clique in cliques:
        for n1 in range(clique[-1] + 1, num_nodes):
            if all(n1 in neighbours[n0] for n0 in clique):
                cliques_new.append(clique + (n1,))
    if len(cliques_new) == 0: break
    cliques = cliques_new
    if length == 3:
        solution_1 = sum(any(nodes[n][0] == "t" for n in c) for c in cliques)


print("Part 1:", solution_1)
print("Part 2:", ",".join(map(nodes.get, cliques[0])))
