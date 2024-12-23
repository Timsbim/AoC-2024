from collections import Counter


print("Day 23")
EXAMPLE = False

file_name = f"2024/input/day_23{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    EDGES = tuple(tuple(line.rstrip().split("-")) for line in file)

# Preliminary reasoning:
graph = {} 
for n0, n1 in EDGES:
    if n0 != n1:
        graph.setdefault(n0, set()).add(n1)
        graph.setdefault(n1, set()).add(n0)
# All nodes have exactly 4/13 neighbours
lengths = set(map(len, graph.values()))
assert len(lengths) == 1 and lengths.pop() == (4 if EXAMPLE else 13)
# A clique of size k implies that each node in it has at least k-1 neighbours:
#  => a maximum clique has a size <= 5/14
#  => if there would be a clique of size 5/14 then the clique would be an
#     isolated subgraph, ie. that neighbourhood would occur exactly 5/14 times
neighbourhoods = {}
for n, ns in graph.items():
    hood = tuple(sorted(ns | {n}))
    neighbourhoods[hood] = neighbourhoods.get(hood, 0) + 1
assert (5 if EXAMPLE else 14) not in Counter(neighbourhoods.values())
# => A maximum clique has exactly 4/13 members!
size = (4 if EXAMPLE else 13)

# Solution
to_str = {i: n for i, n in enumerate(sorted({n for e in EDGES for n in e}))}
to_int = {n: i for i, n in to_str.items()}
graph = {n: set() for n in to_str} 
for n0, n1 in sorted((to_int[n0], to_int[n1]) for n0, n1 in EDGES):
    if n0 < n1:
        graph[n0].add(n1)
    else:
        graph[n1].add(n0)
bases = tuple(set(range(i + 1, len(graph))) for i in range(len(graph)))

# Part 1
start, cliques = [(n0, n1) for n0, ns in graph.items() for n1 in ns], []
for clique in start:
    base = bases[clique[-1]].intersection(*(graph[n] for n in clique))
    cliques.extend(clique + (n,) for n in base)
solution_1 = sum(any(to_str[n][0] == "t" for n in c) for c in cliques)

# Part 2
while cliques:
    clique = cliques.pop()
    if len(clique) == size:
        solution_2 = ",".join(map(to_str.get, clique))
        break
    base = bases[clique[-1]].intersection(*(graph[n] for n in clique))
    cliques.extend(clique + (n,) for n in base)

print("Part 1:", solution_1)
print("Part 2:", solution_2)
