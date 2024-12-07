print(f"Day 6")
EXAMPLE = False

file_name = f"2024/input/day_06"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"
with open(file_name, "r") as file:
    grid = tuple(line.rstrip() for line in file)
ROWS, COLS = len(grid), len(grid[0])
obstacles = set()
for r, line in enumerate(grid):
    for c, char in enumerate(line):
        if char == ".":
            continue
        if char == "#":
            obstacles.add((r, c))
        else:
            start, direction = (r, c), char

DIRECTION = dict(zip("^>v<", range(4)))
DELTA = (-1, 0), (0, 1), (1, 0), (0, -1)

visited, (r, c), d = {start}, start, DIRECTION[direction]
while True:
    dr, dc = DELTA[d]
    r1, c1 = r + dr, c + dc
    if r1 < 0 or r1 == ROWS or c1 < 0 or c1 == COLS:
        break
    if (r1, c1) in obstacles:
        d = (d + 1) % 4
    else:
        r, c = r1, c1
        visited.add((r, c)) 
print(f"Part 1: {len(visited)}")

count, d_start = 0, DIRECTION[direction]
for position in visited - {start}:
    obstacles_mod = obstacles | {position}
    (r, c), d = start, d_start
    visited_mod = {(r, c, d)}
    while True:
        dr, dc = DELTA[d]
        r1, c1 = r + dr, c + dc
        if r1 < 0 or r1 == ROWS or c1 < 0 or c1 == COLS:
            break
        if (r1, c1) in obstacles_mod:
            d = (d + 1) % 4
        else:
            r, c = r1, c1
        if (r, c, d) in visited_mod:
            count += 1
            break
        visited_mod.add((r, c, d))
print(f"Part 2: {count}")
