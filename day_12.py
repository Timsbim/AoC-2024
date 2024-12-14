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

ds = (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)
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
                for i in range(0, 7, 2):
                    dr, dc = ds[i]
                    s = r + dr, c + dc
                    if s in rest:
                        rest.remove(s)
                        rim_new.add(s)
                    if s not in spots:
                        fences += 1
                        (dr2, dc2), (dr1, dc1) = ds[i-2], ds[i-1]
                        b2 = (r + dr2, c + dc2) not in spots
                        b1 = (r + dr1, c + dc1) not in spots
                        if b2 or not (b2 or b1):
                            sides += 1                             
            rim = rim_new
        count_1 += count * fences
        count_2 += count * sides
    
print(f"Part 1: {count_1}")
print(f"Part 2: {count_2}")
