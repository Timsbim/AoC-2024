print("Day 10")
EXAMPLE = False

file_name = "2024/input/day_10"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"
with open(file_name, "r") as file:
    topos = tuple(tuple(map(int, line.rstrip())) for line in file)

ROWS, COLS = len(topos), len(topos[0])


def moves(r, c):
    for dr, dc in (0, 1), (1, 0), (0, -1), (-1, 0):
        r1, c1 = r + dr, c + dc
        if 0 <= r1 < ROWS and 0 <= c1 < COLS:
            yield r1, c1


score = count = 0
for r0, row in enumerate(topos):
    for c0, n in enumerate(row):
        if n: continue
        heads = [(r0, c0)]
        for n in range(1, 10):
            heads_new = []
            for r, c in heads:
                for r1, c1 in moves(r, c):
                    if topos[r1][c1] == n:
                        heads_new.append((r1, c1))
            heads = heads_new
        score += len(set(heads))
        count += len(heads)

print(f"Part 1: {score}")
print(f"Part 2: {count}")
