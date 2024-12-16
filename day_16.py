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
    if minimum < cost:
        continue
    if path[-1] == END:
        if cost < minimum:
            minimum, seats = cost, set(path)
        else:
            seats.update(path)
        continue
    (r, c), (dr, dc) = path[-1], DELTA[d]
    if (cost_new := cost + 1) <= minimum:
        if GRID[r1 := r + dr, c1 := c + dc] != "#":
            p1 = r1, c1
            pd = p1, d
            if cost_new <= visited.get(pd, INF):
                paths.append((path + (p1,), d, cost_new))
                visited[pd] = cost_new
    if (cost_new := cost + 1_000) <= minimum:
        for d1 in (d - 1) % 4, (d + 1) % 4:
            pd = path[-1], d1
            if cost_new <= visited.get(pd, INF):
                paths.append((path, d1, cost_new))
                visited[pd] = cost_new
solution_1, solution_2 = minimum, len(seats)

print(f"Part 1: {solution_1}")
print(f"Part 2: {solution_2}")
