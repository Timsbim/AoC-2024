print("Day 12")
EXAMPLE = False

file_name = f"2024/input/day_12"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"
with open(file_name, "r") as file:
    plants = {}
    for r, row in enumerate(file):
        for c, plant in enumerate(row.rstrip()):
            plants.setdefault(plant, set()).add((r, c))

DIRS = (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)
count_1 = count_2 = 0
for p, spots in plants.items():
    rest = set(spots)
    while rest:
        s = rest.pop()
        count = fences = sides = 0
        rim = {s}
        while rim:
            count += len(rim)
            rim_new = set()
            for r, c in rim:
                ds, cs = [], []
                for dr, dc in DIRS:
                    ds.append((r + dr, c + dc))
                    cs.append(ds[-1] not in spots)
                for i in range(0, 7, 2):
                    s = ds[i]
                    if s in rest:
                        rest.remove(s)
                        rim_new.add(s)
                    if s not in spots:
                        fences += 1
                        if cs[i-2] or not (cs[i-2] or cs[i-1]):
                            sides += 1
            rim = rim_new
        count_1 += count * fences
        count_2 += count * sides
    
print(f"Part 1: {count_1}")
print(f"Part 2: {count_2}")
