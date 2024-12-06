import re


print("Day 3")
EXAMPLE = False

if EXAMPLE:
    memory = (
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+"
        "mul(32,64](mul(11,8)undo()?mul(8,5))"
    )
else:
    with open("2024/input/day_03.txt", "r") as file:
        memory = file.read().rstrip()

re_mul = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
solution = sum(int(m[1]) * int(m[2]) for m in re_mul.finditer(memory))
print(f"Part 1: {solution}")

re_trim = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")
solution, mul = 0, True
for m in re_trim.finditer(memory):
    if m[0] == "do()":
        mul = True
    elif m[0] == "don't()":
        mul = False
    elif mul:
        solution += int(m[1]) * int(m[2])
print(f"Part 2: {solution}")
