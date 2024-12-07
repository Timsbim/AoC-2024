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


def solve(ops, test, numbers, res):        
    n, *numbers = numbers
    if len(numbers) == 0:
        return any(op(res, n) == test for op in ops)
    for op in ops:
        if (res1 := op(res, n)) <= test and solve(ops, test, numbers, res1):
            return True
    return False


ops = add, mul
solution = sum(test for test, (n, *ns) in equations if solve(ops, test, ns, n))
print(f"Part 1: {solution}")

def concat(n, m): return int(f"{n}{m}")
ops = add, mul, concat
solution = sum(test for test, (n, *ns) in equations if solve(ops, test, ns, n))
print(f"Part 2: {solution}")
