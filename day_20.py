print("Day 20")
EXAMPLE = False

file_name = f"2024/input/day_20{'_example' if EXAMPLE else ''}.txt"
GRID = set()
with open(file_name, "r") as file:
    for r, line in enumerate(file):
        for c, char in enumerate(line):
            if char == "S":
                START = r, c
            elif char == "E":
                END = r, c
            elif char == "#":
                GRID.add((r, c))
THRESHOLD = 50 if EXAMPLE else 100


def on_the_edge(p, dist):
    """ Counting is symmetric => only one half necesarry """
    r, c = p
    yield r + dist, c 
    for dr in range(1, dist):
        dc = dist - dr
        yield r + dr, (c1 := c + dc)
        yield r - dr, c1
    yield r, c + dist


path = [None, START]
while path[-1] != END:
    r, c = path[-1]
    for dr, dc in (0, 1), (1, 0), (-1, 0), (0, -1):
        p = r + dr, c + dc
        if p != path[-2] and p not in GRID:
            path.append(p)
            break
path = {p: n for n, p in enumerate(path[1:])}
count_1 = count_2 = 0
for p0, t0 in path.items():
    for dist in range(2, 21):
        for p1 in on_the_edge(p0, dist):
            if p1 in path and abs(path[p1] - t0) - dist >= THRESHOLD:
                if dist == 2:
                    count_1 += 1
                else:
                    count_2 += 1                        

print(f"Part 1: {count_1}")
print(f"Part 2: {count_1 + count_2}")
