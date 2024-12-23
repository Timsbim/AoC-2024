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

# Part 1
cliques = set()
for n0, ns in graph.items():
    for n1 in ns:
        for n2 in graph[n1]:
            if n2 in graph[n0]:
                cliques.add(tuple(sorted([n0, n1, n2])))
solution_1 = sum(any(n[0] == "t" for n in c) for c in cliques)

# Part 2
counts = Counter()
for n, ns in graph.items():
    ns = sorted([n, *ns])
    for i in range(len(ns)):
        counts[tuple(ns[:i] + ns[i+1:])] += 1
ns, _ = counts.most_common(1).pop()
solution_2 = ",".join(ns)

print("Part 1:", solution_1)
print("Part 2:", solution_2)
