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

minimum, paths, dists = INF, [(START, 0, 0)], {(START, 0): 0}
while paths:
    paths_new = []
    for (r, c), d, cost in paths:
        for d, add in (d, 1), ((d - 1) % 4, 1_001), ((d + 1) % 4, 1_001):
            if (cost_new := cost + add) < minimum:
                dr, dc = DELTA[d]
                if GRID[p := (r + dr, c + dc)] != "#":
                    if p == END:
                        minimum = cost_new
                    elif cost_new < dists.get(pd := (p, d), INF):
                        paths_new.append((p, d, cost_new))
                        dists[pd] = cost_new
    paths = paths_new
print(f"Part 1: {minimum}")

seats, paths = set(), [((START,), 0, 0)]
while paths:
    path, d, cost = paths.pop()
    r, c = path[-1]
    for d, add in (d, 1), ((d - 1) % 4, 1_001), ((d + 1) % 4, 1_001):
        if (cost_new := cost + add) <= minimum:
            dr, dc = DELTA[d]
            if GRID[p := (r + dr, c + dc)] != "#":
                path_new = path + (p,)
                if cost_new == minimum:
                    if p == END:
                        seats.update(path_new)
                    continue
                if cost_new <= dists[p, d]:
                    paths.append((path_new, d, cost_new))
print(f"Part 2: {len(seats)}")
