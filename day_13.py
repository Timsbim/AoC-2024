import re


print("Day 13")
EXAMPLE = True

file_name = "2024/input/day_13"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"
re_xy = re.compile("X(?:\+|=)(\d+), Y(?:\+|=)(\d+)")
with open(file_name, "r") as file:
    blocks = file.read().split("\n\n")
machines = []
for block in blocks:
    machines.append(tuple(
        tuple(map(int, re_xy.search(line).groups()))
        for line in block.splitlines()
    ))
machines = tuple(machines)


def det(x, y):
    return x[0] * y[1] - x[1] * y[0]


def costs(a, b, p):
    if (d := det(a, b)) != 0:
        da, db = det(p, b), det(a, p)
        na, nb = da // d, db // d
        if all(na * a[i] + nb * b[i] == p[i] for i in (0, 1)):
            return na * 3 + nb

    n = None
    if all(a[i] != 0 for i in (0, 1)):
        n0, n1 = (p[i] // a[i] for i in (0, 1))
        if n0 == n1 and all(n0 * a[i] == p[i] for i in (0, 1)):
            n = n0 * 3
    if all(b[i] != 0 for i in (0, 1)):
        n0, n1 = (p[i] // b[i] for i in (0, 1))
        if n0 == n1 and all(n0 * b[i] == p[i] for i in (0, 1)):
            n = min(n, n0) if n is not None else n0    
    
    return n if n is not None else 0


print(f"Part 1: {sum(costs(a, b, p) for a, b, p in machines)}")
s = 10_000_000_000_000
print(f"Part 2: {sum(costs(a, b, (p[0] + s, p[1] + s)) for a, b, p in machines)}")
