# Haven't found out why this works too yet :(
from functools import cache
from itertools import combinations, groupby, product


print("Day 21")
EXAMPLE = False

file_name = f"2024/input/day_21{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    CODES = tuple(file.read().splitlines())

DELTA = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
REV = dict(zip("^v<>A", "v^><A"))

NUM = {
    (r, c): char
    for r, line in enumerate("789|456|123| 0A".split("|"))
    for c, char in enumerate(line)
    if char != " "
}
NUMPAD = dict.fromkeys(zip("0123456789A", "0123456789A"), tuple())
for (r0, c0), (r1, c1) in combinations(NUM, 2):
    k0, k1 = NUM[r0, c0], NUM[r1, c1]
    ver = "v" * dr if (dr := r1 - r0) >= 0 else "^" * abs(dr)
    hor = ">" * dc if (dc := c1 - c0) >= 0 else "<" * abs(dc)
    NUMPAD[k0, k1] = (hor + ver,)
    if (c0 != 0 or r1 != 3) and (dr != 0 and dc != 0):
        NUMPAD[k0, k1] += (ver + hor,)
    NUMPAD[k1, k0] = tuple(
        "".join(REV[c] for c in seq[::-1]) for seq in NUMPAD[k0, k1]
    )

DIRPAD = {
 ('<', '<'): '',
 ('<', '>'): '>>',
 ('<', 'A'): '>>^',
 ('<', '^'): '>^',
 ('<', 'v'): '>',
 ('>', '<'): '<<',
 ('>', '>'): '',
 ('>', 'A'): '^',
 ('>', '^'): '<^',
 ('>', 'v'): '<',
 ('A', '<'): 'v<<',
 ('A', '>'): 'v',
 ('A', 'A'): '',
 ('A', '^'): '<',
 ('A', 'v'): '<v',
 ('^', '<'): 'v<',
 ('^', '>'): 'v>',
 ('^', 'A'): '>',
 ('^', '^'): '',
 ('^', 'v'): 'v',
 ('v', '<'): '<',
 ('v', '>'): '>',
 ('v', 'A'): '^>',
 ('v', '^'): '^',
 ('v', 'v'): ''
}


@cache
def length(path, n):
    if n == 0:
        return len(path)
    count = 0
    for As, group in groupby(path, key=lambda char: char == "A"):
        path = "".join(group)
        if As:
            count += len(path) - 1
            continue
        path = "A".join(map(DIRPAD.get, zip(f"A{path}", f"{path}A")))
        count += length(f"{path}A", n-1)
    return count


def complexity(code, n=2):
    paths = product(*map(NUMPAD.get, zip(f"A{code}", code)))
    paths = ("A".join(path) + "A" for path in paths)
    return int(code.replace("A", "")) * min(length(path, n) for path in paths)


print(f"Part 1: {sum(map(complexity, CODES))}")
print(f"Part 2: {sum(complexity(code, n=25) for code in CODES)}")
