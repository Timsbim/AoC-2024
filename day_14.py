from math import prod


print("Day 14")

robots = []
with open("2024/input/day_14.txt", "r") as file:
    for line in file:
        robots.append(tuple(
            tuple(map(int, reversed(part[2:].split(","))))
            for part in line.split()
        ))
robots = tuple(robots)
ROWS, COLS = 103, 101

positions = tuple(
    ((py + 100 * vy) % ROWS, (px + 100 * vx) % COLS)
    for (py, px), (vy, vx) in robots
)
quadrants = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 0}
m_rows, m_cols = ROWS // 2, COLS // 2
for y, x in positions:
    if y != m_rows and x != m_cols:
        quadrants[int(y < m_rows), int(x < m_cols)] += 1    
print(f"Part 1: {prod(quadrants.values())}")


def contains_frame(positions):
    lines = {}
    for y, x in set(positions):
        lines.setdefault(y, set()).add(x)
    for line in lines.values():
        line = "".join("*" if x in line else " " for x in range(COLS))
        if "*******************************" in line:
              return True
    return False


positions, velocities = zip(*robots)
for s in range(1, 10404):
    positions = tuple(
        ((py + vy) % ROWS, (px + vx) % COLS)
        for (py, px), (vy, vx) in zip(positions, velocities)
    )
    if contains_frame(positions):
        solution = s
        break
print(f"Part 2: {solution}")
