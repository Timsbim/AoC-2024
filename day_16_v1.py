# Find minimum costs (via Dijkstra) and at the same time all corresponding paths
# => Compacter than version 0, but slower!
print("Day 16")
EXAMPLE = False

grid = {}
file_name = f"2024/input/day_16{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    for r, line in enumerate(file):
        for c, char in enumerate(line.rstrip()):
            if char != "#":
                grid.setdefault(char, set()).add((r, c))
start, end = grid["S"].pop(), grid["E"].pop()
grid = grid["."] | {start, end}

DELTA = (0, 1), (1, 0), (0, -1), (-1, 0)
INF = float("inf")

minimum, seats = INF, set()
paths, dists = [((start,), 0, 0)], {(start, 0): 0}
while paths:
    paths_new = []
    for path, d, cost in paths:
        r, c = path[-1]
        for d, add in (d, 1), ((d - 1) % 4, 1_001), ((d + 1) % 4, 1_001):
            if (cost_new := cost + add) <= minimum:
                dr, dc = DELTA[d]
                if (p := (r + dr, c + dc)) in grid:
                    if p == end:
                        if cost_new < minimum:
                            minimum, seats = cost_new, set(path)
                        else:
                            seats.update(path)
                        continue
                    if cost_new == minimum:
                        continue
                    if cost_new <= dists.get(pd := (p, d), INF):
                        paths_new.append((path + (p,), d, cost_new))
                        dists[pd] = cost_new
    paths = paths_new

print(f"Part 1: {minimum}")
print(f"Part 2: {len(seats) + 1}")
