from functools import cmp_to_key, partial


print("Day 5")
EXAMPLE = False

file_name = f"2024/input/day_05"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

with open(file_name, "r") as file:
    orderings = set()
    while "|" in (line := next(file)):
        orderings.add(tuple(map(int, line.split("|"))))
    updates = tuple(tuple(map(int, line.split(","))) for line in file)


def is_correct(update):
    for i, n in enumerate(update[:-1]):
        for m in update[i+1:]:
            if (n, m) not in orderings:
                return False
    return True


solution = sum(
    update[len(update) // 2] for update in updates if is_correct(update)
)
print(f"Part 1: {solution}")

def cmp(a, b): return 1 if (a, b) in orderings else -1

key = cmp_to_key(cmp)
solution = sum(
    sorted(update, key=key)[len(update) // 2]
    for update in updates
    if not is_correct(update)
)
print(f"Part 2: {solution}")
