from functools import cache


print("Day 11")
EXAMPLE = False

file_name = f"2024/input/day_11{'_example' if EXAMPLE else ''}.txt"
with open("2024/input/day_11.txt", "r") as file:
    arrangement = tuple(file.read().split())


@cache
def count(stone, step=0, max_step=25):
    if step == max_step:
        return 1
    step += 1
    if stone ==  "0":
        return count("1", step, max_step)
    if len(stone) % 2:
        return count(str(int(stone) * 2024), step, max_step)
    m = len(stone) // 2
    count_1 = count(stone[:m], step, max_step)
    return count_1 + count(str(int(stone[m:])), step, max_step)


print(f"Part 1: {sum(count(stone) for stone in arrangement)}")
print(f"Part 2: {sum(count(stone, max_step=75) for stone in arrangement)}")
