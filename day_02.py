print("Day 2")
EXAMPLE = False

file_name = f"2024/input/day_02{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    reports = tuple(tuple(map(int, line.split())) for line in file)


def is_safe(report):
    slope = report[0] < report[1]
    for a, b in zip(report, report[1:]):
        diff = abs(a - b)
        if diff == 0 or 3 < diff or (a < b) != slope:
            return False
    return True


solution = sum(is_safe(report) for report in reports)
print(f"Part 1: {solution}")


def is_safe_mod(report):
    for i in range(len(report)):
        report_mod = report[:i] + report[i+1:]
        if is_safe(report_mod):
            return True
    return False
 

solution = sum(is_safe_mod(report) for report in reports)
print(f"Part 2: {solution}")
