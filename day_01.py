from collections import Counter


print("Day 1")
EXAMPLE = False

file_name = f"2024/input/day_01"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"
with open(file_name, "r") as file:
    numbers = tuple(zip(*(map(int, line.split()) for line in file)))

solution = sum(
    abs(n - m) for n, m in zip(sorted(numbers[0]), sorted(numbers[1]))
)
print(f"Part 1: {solution}")

counts2 = Counter(numbers[1])
solution = sum(n * counts2.get(n, 0) for n in numbers[0])
print(f"Part 2: {solution}")
