# 1. step: find minium costs (via Dijkstra)
# 2. step: find corresponding paths with DFS and using the distance measurements from 1.
# => Faster than version 1!
print("Day 16")
EXAMPLE = False

file_name = f"2024/input/day_16{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    layout = file.read()
grid = set()
for r, row in enumerate(layout.splitlines()):
    for c, char in enumerate(row):
        if char == "S":
            start, char = (r, c), "."
        elif char == "E":
            end, char = (r, c), "."
        if char == ".":
            grid.add((r, c))

DELTA = (0, 1), (1, 0), (0, -1), (-1, 0)
INF = float("inf")

minimum, paths, dists = INF, [(start, 0, 0)], {(start, 0): 0}
while paths:
    paths_new = []
    for (r, c), d, cost in paths:
        for d, add in (d, 1), ((d - 1) % 4, 1_001), ((d + 1) % 4, 1_001):
            if (cost_new := cost + add) < minimum:
                dr, dc = DELTA[d]
                if (p := (r + dr, c + dc)) in grid:
                    if p == end:
                        minimum = cost_new
                    elif cost_new < dists.get(pd := (p, d), INF):
                        paths_new.append((p, d, cost_new))
                        dists[pd] = cost_new
    paths = paths_new
print(f"Part 1: {minimum}")

seats, paths = set(), [((start,), 0, 0)]
while paths:
    path, d, cost = paths.pop()
    r, c = path[-1]
    for d, add in (d, 1), ((d - 1) % 4, 1_001), ((d + 1) % 4, 1_001):
        if (cost_new := cost + add) <= minimum:
            dr, dc = DELTA[d]
            if (p := (r + dr, c + dc)) in grid:
                path_new = path + (p,)
                if cost_new == minimum:
                    if p == end:
                        seats.update(path_new)
                    continue
                if cost_new == dists[p, d]:
                    paths.append((path_new, d, cost_new))
print(f"Part 2: {len(seats)}")
