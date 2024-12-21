from functools import cache
from itertools import combinations, groupby


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
NUMPAD = {}
for (r0, c0), (r1, c1) in combinations(NUM, 2):
    if r0 == r1 and c0 == c1: continue
    k0, k1 = NUM[r0, c0], NUM[r1, c1]
    dr, dc = r1 - r0, c1 - c0
    ver = "^" * abs(dr) if dr < 0 else "v" * dr
    hor = "<" * abs(dc) if dc < 0 else ">" * dc
    if c0 == 0 and r1 == 3:
        NUMPAD[k0, k1] = {hor + ver}
    else:
        NUMPAD[k0, k1] = {hor + ver, ver + hor}    
    NUMPAD[k1, k0] = {
        "".join(REV[c] for c in seq[::-1]) for seq in NUMPAD[k0, k1]
    }

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
        return len(path) - 1
    count = 0
    for take, group in groupby(path, key=lambda char: char != "A"):
        path = "".join(group)
        if not take:
            count += len(path) - 1
            continue
        path = f"A{path}A"
        path = "".join(f"{DIRPAD[a, b]}A" for a, b in zip(path, path[1:]))
        count += length(f"A{path}", n-1)
    return count


def complexity(code, n=2):
    code = f"A{code}"
    paths = {"A"}
    for a, b in zip(code, code[1:]):
        paths_new = set()
        for part in NUMPAD[a, b]:
            for path in paths:
                paths_new.add(f"{path}{part}A")
        paths = paths_new
    num = int(code.replace("A", ""))
    return num * min(length(path, n) for path in paths)


solution_1 = sum(complexity(code) for code in CODES)
solution_2 = sum(complexity(code, n=25) for code in CODES)
print(f"Part 1: {solution_1}")
print(f"Part 2: {solution_2}")
assert solution_1 == (126384 if EXAMPLE else 152942)
assert solution_2 == (154115708116294 if EXAMPLE else 189235298434780)
