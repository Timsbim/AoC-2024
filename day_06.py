print(f"Day 6")
EXAMPLE = False

DIRECTION = dict(zip(">v<^", range(4)))
DELTA = (0, 1), (1, 0), (0, -1), (-1, 0)

file_name = f"2024/input/day_06{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    grid = tuple(line.rstrip() for line in file)
ROWS, COLS = len(grid), len(grid[0])
obstacles = set()
for r, line in enumerate(grid):
    for c, char in enumerate(line):
        if char == ".": continue
        if char == "#":
            obstacles.add((r, c))
        else:
            start, direction = (r, c), DIRECTION[char]

visited, (r, c), d = {start}, start, direction
while True:
    (dr, dc), d1 = DELTA[d], d
    while 0 <= (r1 := r + dr) < ROWS and 0 <= (c1 := c + dc) < COLS:
        if (r1, c1) in obstacles:
            d1 = (d + 1) % 4
            break
        r, c = r1, c1
        visited.add((r, c))
    if d1 == d: break
    d = d1
print(f"Part 1: {len(visited)}")

count = 0
for position in visited - {start}:
    obstacles_mod = obstacles | {position}
    (r, c), d = start, direction
    visited = {(r, c, d)}
    while True:
        (dr, dc), d1 = DELTA[d], d
        while 0 <= (r1 := r + dr) < ROWS and 0 <= (c1 := c + dc) < COLS:
            if (r1, c1) in obstacles_mod:
                d1 = (d + 1) % 4
                break
            r, c = r1, c1
        if d1 == d: break
        d = d1
        if (r, c, d) in visited:
            count += 1
            break
        visited.add((r, c, d))
print(f"Part 2: {count}")
