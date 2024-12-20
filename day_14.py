""" Pro tipp: the first part is more often than not very helpful! The safety
 factor of evenly distributed positions is roughly 240_000_000. So a threshold
 that is low enough will point out anomalies.
"""
from math import prod


print("Day 14")
EXAMPLE = False

positions, velocities = [], []
file_name = f"2024/input/day_14{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    for line in file:
        position, velocity = line.split()
        x, y = map(int, position[2:].split(","))
        positions.append((y, x))
        vx, vy = map(int, velocity[2:].split(","))
        velocities.append((vy, vx))
POSITIONS, VELOCITIES = tuple(positions), tuple(velocities)
ROWS, COLS = (7, 11) if EXAMPLE else (103, 101)
ROWS_M, COLS_M = ROWS // 2, COLS // 2


def safety_factor(positions):
    quadrants = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 0}
    for y, x in positions:
        if y != ROWS_M and x != COLS_M:
            quadrants[int(y < ROWS_M), int(x < COLS_M)] += 1    
    return prod(quadrants.values())


solution = safety_factor(
    ((py + 100 * vy) % ROWS, (px + 100 * vx) % COLS)
    for (py, px), (vy, vx) in zip(POSITIONS, VELOCITIES)
)
print(f"Part 1: {solution}")

positions = POSITIONS
for second in range(1, 10404):
    positions = tuple(
        ((py + vy) % ROWS, (px + vx) % COLS)
        for (py, px), (vy, vx) in zip(positions, VELOCITIES)
    )
    if safety_factor(positions) < 100_000_000:
        break
print(f"Part 2: {second}")
