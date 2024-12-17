from collections import Counter
from functools import cache


print("Day 11")
EXAMPLE = False

file_name = f"2024/input/day_11{'_example' if EXAMPLE else ''}.txt"
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


def count(counts, steps):
    for _ in range(steps):
        counts_new = Counter()
        for stone, n in counts.items():
            for stone in blink(stone):
                counts_new[stone] += n
        counts = counts_new
    return counts


print(f"Part 1: {(counts := count(Counter(arrangement), 25)).total()}")
print(f"Part 2: {count(counts, 50).total()}")
