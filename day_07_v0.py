from functools import partial
from operator import add, mul


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
equations = tuple(equations)


def solve(ops, test, numbers):
    length, stack = len(numbers), [(1, numbers[0])]
    while stack:
        i, res0 = stack.pop()
        n, i = numbers[i], i + 1
        for op in ops:
            res1 = op(res0, n)
            if i == length:
                if res1 == test:
                    return True
            elif res1 <= test:
                stack.append((i, res1))
    return False


check = partial(solve, (add, mul))
solution = sum(test for test, numbers in equations if check(test, numbers))
print(f"Part 1: {solution}")

def concat(n, m): return int(f"{n}{m}")
check = partial(solve, (add, mul, concat))
solution = sum(test for test, numbers in equations if check(test, numbers))
print(f"Part 2: {solution}")
