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
    files[i], files[j] = files[j], "."
solution = checksum(files)
print(f"Part 1: {solution}")

ID, files, occupied, free = -1, [], {}, {}
for i, n in enumerate(disk_map):
    l, n, = len(files), int(n)
    container, key, item = (free, l, ".") if i % 2 else (occupied, ID := ID + 1, ID)
    container[key] = range(l, l + n)
    files.extend(item for _ in range(n))
occupied = [*occupied.items()]
while occupied:
    ID, idxso = occupied.pop()
    i, l, found = idxso.start, len(idxso), False
    for j, idxsf in free.items():
        if i <= idxsf.start:
            break
        if l <= len(idxsf):
            found = True
            break
    if found:
        for k, l in zip(idxsf, idxso):
            files[k], files[l] = ID, "."
        if len(idxso) < len(idxsf):
            free[j] = range(idxsf.start + len(idxso), idxsf.stop)
        else:
            del free[j]
solution = checksum(files)
print(f"Part 2: {solution}")
