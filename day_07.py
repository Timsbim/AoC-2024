from functools import partial
from operator import add, mul
from pprint import pprint


print("Day 7")
EXAMPLE = False

file_name = f"2024/input/day_07"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"

with open(file_name, "r") as file:
    equations = []
    for line in file:
        test, numbers = line.split(": ")
        equations.append((int(test), tuple(map(int, numbers.split()))))


def solve(ops, test, numbers):
    length, stack = len(numbers), [(1, numbers[0])]
    while stack:
        i, n = stack.pop()
        if i == length and n == test:
            return True
        if i < length:
            for op in ops:
                m = op(n, numbers[i])
                if m <= test:
                    stack.append((i + 1, m))
    return False


check = partial(solve, (add, mul))
solution = sum(test for test, numbers in equations if check(test, numbers))
print(f"Part 1: {solution}")

def concat(n, m): return int(f"{n}{m}")
check = partial(solve, (add, mul, concat))
solution = sum(test for test, numbers in equations if check(test, numbers))
print(f"Part 2: {solution}")
