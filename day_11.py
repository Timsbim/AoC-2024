from functools import cache


print("Day 11")
EXAMPLE = False

if EXAMPLE:
    arrangement = tuple("125 17".split())
else:
    with open("2024/input/day_11.txt", "r") as file:
        arrangement = tuple(file.read().split())

@cache
def count(stone, step=0, max_step=25):
    if step == max_step:
        return 1
    step = step + 1
    if stone ==  "0":
        return count("1", step, max_step)
    elif len(stone) % 2 == 0:
        m = len(stone) // 2
        return (
            count(stone[:m], step, max_step)
            + count(str(int(stone[m:])), step, max_step)
        )
    else:
        return count(str(int(stone) * 2024), step, max_step)


solution = sum(count(stone) for stone in arrangement)
print(f"Part 1: {solution}")
solution = sum(count(stone, max_step=75) for stone in arrangement)
print(f"Part 2: {solution}")
