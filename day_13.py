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
        na, nb = da / d, db / d
        if na.is_integer() and nb.is_integer():
            return int(na) * 3 + int(nb)
    if (
        (n0 := p[0] / b[0]).is_integer()
        and (n1 := p[1] / b[1]).is_integer()
        and (n := int(n0)) == int(n1) 
    ):
        return n
    if (
        (n0 := p[0] / a[0]).is_integer()
        and (n1 := p[1] / a[1]).is_integer()
        and (n := int(n0)) == int(n1)
    ):
        return n * 3
    return 0


print(f"Part 1: {sum(costs(a, b, p) for a, b, p in machines)}")
s = 10_000_000_000_000
print(f"Part 2: {sum(costs(a, b, (p[0] + s, p[1] + s)) for a, b, p in machines)}")
