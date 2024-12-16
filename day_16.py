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
paths, visited = [((START,), 0, 0)], {(START, 0): 0}
while paths:
    path, d, cost = paths.pop()
    r, c = path[-1]
    for d_new, addon in (d, 1), ((d - 1) % 4, 1_001), ((d + 1) % 4, 1_001):
        if (cost_new := cost + addon) <= minimum:
            dr, dc = DELTA[d_new]
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
                if cost_new <= visited.get(pd := (p, d_new), INF):
                    paths.append((path_new, d_new, cost_new))
                    visited[pd] = cost_new
solution_1, solution_2 = minimum, len(seats)

print(f"Part 1: {solution_1}")
print(f"Part 2: {solution_2}")
