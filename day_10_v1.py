# Find minimum costs (via Dijkstra) and at the same time all corresponding paths
# => Compacter than version 0, but slower!
print("Day 16")

EXAMPLE = False

file_name = f"2024/input/day_16{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    layout = file.read()
GRID = {}
for r, row in enumerate(layout.splitlines()):
    for c, char in enumerate(row):
        if char == "S":
            START, char = (r, c), "."
        elif char == "E":
            END, char = (r, c), "."
        GRID[r, c] = char

DELTA = (0, 1), (1, 0), (0, -1), (-1, 0)
INF = float("inf")

minimum, seats = INF, set()
paths, dists = [((START,), 0, 0)], {(START, 0): 0}
while paths:
    paths_new = []
    for path, d, cost in paths:
        r, c = path[-1]
        for d, add in (d, 1), ((d - 1) % 4, 1_001), ((d + 1) % 4, 1_001):
            if (cost_new := cost + add) <= minimum:
                dr, dc = DELTA[d]
                if GRID[p := (r + dr, c + dc)] != "#":
                    path_new = path + (p,)
                    if p == END:
                        if cost_new < minimum:
                            minimum, seats = cost_new, set(path_new)
                        else:
                            seats.update(path_new)
                        continue
                    if cost_new == minimum:
                        continue
                    if cost_new <= dists.get(pd := (p, d), INF):
                        paths_new.append((path_new, d, cost_new))
                        dists[pd] = cost_new
    paths = paths_new

print(f"Part 1: {minimum}")
print(f"Part 2: {len(seats)}")
