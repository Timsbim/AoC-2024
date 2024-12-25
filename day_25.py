print("Day 25")
EXAMPLE = False

file_name = f"2024/input/day_25{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    blocks = file.read().split("\n\n")
keys, locks = [], []
for block in blocks:
    block = block.rstrip().splitlines()
    if block[0] == "#####":
        locks.append(tuple(zip(*block[1:])))
    else:
        keys.append(tuple(zip(*block[:-1])))

count, heights = 0, {}
for key in keys:
    k_heights = tuple(col.count("#") for col in key)
    for lock in locks:
        l_heights = heights.get(lock)
        if l_heights is None:
            heights[lock] = l_heights = tuple(col.count("#") for col in lock)
        count += all(h0 + h1 <= 5 for h0, h1 in zip(k_heights, l_heights))    

print("Part 1:", count)
