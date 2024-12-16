# 1. step: find minium costs (via Dijkstra)
# 2. step: find corresponding paths with DFS and using the distance measurements from 1.
# => Faster than version 1!
print("Day 16")
EXAMPLE = False

file_name = f"2024/input/day_16{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    layout = file.read()
grid = {}
for r, row in enumerate(layout.splitlines()):
    for c, char in enumerate(row):
        if char != "#":
            grid.setdefault(char, set()).add((r, c))
start, end = grid["S"].pop(), grid["E"].pop()
grid = grid["."] | {start, end}

DELTA = (0, 1), (1, 0), (0, -1), (-1, 0)
INF = float("inf")

minimum, paths, dists = INF, [(start, 0, 0)], {(start, 0): 0}
while paths:
    paths_new = []
    for (r, c), d, cost in paths:
        for d, add in (d, 1), ((d - 1) % 4, 1_001), ((d + 1) % 4, 1_001):
            if (cost_new := cost + add) >= minimum: continue
            dr, dc = DELTA[d]
            if (((p := (r + dr, c + dc)) in grid
                    and cost_new < dists.get((p, d), INF))):
                dists[p, d] = cost_new
                if p == end:
                    minimum = cost_new
                else:
                    paths_new.append((p, d, cost_new))
    paths = paths_new
print(f"Part 1: {minimum}")

seats, paths = {end}, [((start,), 0, 0)]
while paths:
    path, d, cost = paths.pop()
    r, c = path[-1]
    for d, add in (d, 1), ((d - 1) % 4, 1_001), ((d + 1) % 4, 1_001):
        if (cost_new := cost + add) <= minimum:
            dr, dc = DELTA[d]
            if (p := (r + dr, c + dc)) in grid and cost_new == dists[p, d]:
                    if p == end:
                        seats.update(path)
                    else:
                        paths.append((path + (p,), d, cost_new))
print(f"Part 2: {len(seats)}")
