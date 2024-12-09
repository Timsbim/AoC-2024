print("Day 9")
EXAMPLE = False

if EXAMPLE:
    disk_map = "2333133121414131402"
else:
    with open("2024/input/day_09.txt", "r") as file:
        disk_map = file.read().rstrip()


def checksum(disk):
    s = 0
    for i, n in enumerate(disk):
        if n != ".":
            s += i * n
    return s


ID, files, occupied, free = -1, [], [], []
for i, n in enumerate(disk_map):
    container, item = (free, ".") if i % 2 else (occupied, ID := ID + 1)
    l, n, = len(files), int(n)
    container.extend(range(l, l + n))
    files.extend(item for _ in range(n))
for i, j in zip(free, reversed(occupied)):
    if j < i:
        break
    files[i] = files[j]
    files[j] = "."
solution = checksum(files)
print(f"Part 1: {solution}")

ID, files, occupied, free = -1, [], [], {}
for i, n in enumerate(disk_map):
    l, n, = len(files), int(n)
    idxs = range(l, l + n)
    if i % 2:
        item, free[l] = ".", idxs
    else:
        item = (ID := ID + 1)
        occupied.append((ID, idxs))
    files.extend(item for _ in range(n))
while occupied:
    ID, idxs = occupied.pop()
    j, l, found = idxs.start, len(idxs), False
    for i, idxs1 in free.items():
        if j <= idxs1.start:
            break
        if l <= len(idxs1):
            found = True
            break
    if found:
        for k, l in zip(free[i], idxs):
            files[k], files[l] = ID, "."
        if len(idxs) < len(free[i]):
            free[i] = range(free[i].start + len(idxs), free[i].stop)
        else:
            del free[i]
solution = checksum(files)
print(f"Part 2: {solution}")
