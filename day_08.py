from itertools import combinations


print("Day 8")
EXAMPLE = False

file_name = "2024/input/day_08"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"
antennas = {}
with open(file_name, "r") as file:
    lines = [line.rstrip() for line in file]
ROWS, COLS = len(lines), len(lines[0])
for r, line in enumerate(lines):
    for c, char in enumerate(line):
        if char != ".":
            antennas.setdefault(char, []).append((r, c))

antinodes = set()
for positions in antennas.values():
    for (r1, c1), (r2, c2) in combinations(positions, 2):
        for r, c in (2 * r1 - r2, 2 * c1 - c2), (2 * r2 - r1, 2 * c2 - c1):
            if 0 <= r < ROWS and 0 <= c < COLS:
                antinodes.add((r, c))
solution = len(antinodes)
print(f"Part 1: {solution}")

antinodes = set()
for positions in antennas.values():
    for (r1, c1), (r2, c2) in combinations(positions, 2):
        for r, c, dr, dc in (r1, c1, r1 - r2, c1 - c2), (r2, c2, r2 - r1, c2 - c1):
            while 0 <= r < ROWS and 0 <= c < COLS:
                antinodes.add((r, c))
                r, c = r + dr, c + dc
solution = len(antinodes)
print(f"Part 2: {solution}")
