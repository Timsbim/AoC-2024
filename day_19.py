from functools import cache


print("Day 19")
EXAMPLE = False

file_name = f"2024/input/day_19{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    patterns, designs =  file.read().split("\n\n")
PATTERNS = set(patterns.split(", "))


@cache
def accounting(design):
    return (1 if design in PATTERNS else 0) + sum(
        accounting(design[len(pattern):])
        for pattern in PATTERNS
        if design.startswith(pattern)
    )


counts = [*map(accounting, designs.splitlines())]
print(f"Part 1: {sum(map(bool, counts))}")
print(f"Part 2: {sum(counts)}")