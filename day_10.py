print("Day 10")
EXAMPLE = False

file_name = "2024/input/day_10"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"
with open(file_name, "r") as file:
    topos = {
        (r, c): n
        for r, line in enumerate(file)
        for c, n in enumerate(map(int, line.rstrip()))
    }

score = count = 0
for (r0, c0), n in topos.items():
    if n: continue
    heads = [(r0, c0)]
    for n in range(1, 10):
        heads_new = []
        for r, c in heads:
            for dr, dc in (0, 1), (1, 0), (0, -1), (-1, 0):
                r1, c1 = r + dr, c + dc
                if topos.get((r1, c1), -1) == n:
                    heads_new.append((r1, c1))
        heads = heads_new
    score += len(set(heads))
    count += len(heads)

print(f"Part 1: {score}")
print(f"Part 2: {count}")
