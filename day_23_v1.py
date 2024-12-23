print("Day 23")
EXAMPLE = False

file_name = f"2024/input/day_23{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    EDGES = tuple(tuple(line.rstrip().split("-")) for line in file)

to_str = {i: n for i, n in enumerate(sorted({n for e in EDGES for n in e}))}
to_int = {n: i for i, n in to_str.items()}
graph = {n: set() for n in to_str} 
for n0, n1 in sorted((to_int[n0], to_int[n1]) for n0, n1 in EDGES):
    if n0 < n1:
        graph[n0].add(n1)
    else:
        graph[n1].add(n0)
bases = tuple(set(range(i + 1, len(graph))) for i in range(len(graph)))
cliques = [(n0, n1) for n0, ns in graph.items() for n1 in ns]
for length in range(3, len(graph)):
    cliques_new = []
    for clique in cliques:
        base = bases[clique[-1]].intersection(*(graph[n] for n in clique))
        cliques_new.extend(clique + (n,) for n in base)
    if len(cliques_new) == 0: break
    cliques = cliques_new
    if length == 3:
        solution_1 = sum(any(to_str[n][0] == "t" for n in c) for c in cliques)

print("Part 1:", solution_1)
print("Part 2:", ",".join(map(to_str.get, cliques[0])))
