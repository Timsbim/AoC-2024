from collections import Counter
from functools import cache


print("Day 11")
EXAMPLE = False

if EXAMPLE:
    arrangement = tuple("125 17".split())
else:
    with open("2024/input/day_11.txt", "r") as file:
        arrangement = tuple(file.read().split())


@cache
def blink(stone):
    if stone ==  "0":
        return ("1",)
    if len(stone) % 2:
        return (str(int(stone) * 2024),)
    m = len(stone) // 2
    return stone[:m], str(int(stone[m:]))


def count(arrangement, steps):
    counts = Counter(arrangement)
    for _ in range(steps):
        counts_new = Counter()
        for stone, n in counts.items():
            for stone in blink(stone):
                counts_new[stone] += n
        counts = counts_new
    return counts.total()


print(f"Part 1: {count(arrangement, 25)}")
print(f"Part 2: {count(arrangement, 75)}")
