from functools import cache


print("Day 19")
EXAMPLE = False

file_name = f"2024/input/day_19{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    patterns, designs =  file.read().split("\n\n")
PATTERNS = set(patterns.split(", "))
designs = tuple(designs.splitlines())


@cache
def accounting(design):
    return (1 if design in PATTERNS else 0) + sum(
        accounting(design[len(pattern):])
        for pattern in PATTERNS
        if design.startswith(pattern)
    )


count_1 = count_2 = 0
for design in designs:
    count = accounting(design)
    if count:
        count_1 += 1
        count_2 += count

print(f"Part 1: {count_1}")
print(f"Part 2: {count_2}")
