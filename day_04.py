print("Day 4")
EXAMPLE = False

file_name = f"2024/input/day_04"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"
with open(file_name, "r") as file:
    lines = [line.rstrip() for line in file]
if EXAMPLE:
    pprint(lines)
ROWS, COLS = len(lines), len(lines[0])


def count(line):
    return line.count("XMAS") + line.count("SAMX")


solution = (
    sum(count(line) for line in lines)
    + sum(count("".join(line)) for line in zip(*lines))
    + sum(
        count("".join(lines[d+c][c] for c in range(min(ROWS - d, COLS))))
        for d in range(ROWS)
    )
    + sum(
        count("".join(lines[r][r+d] for r in range(min(COLS - d, ROWS))))
        for d in range(1, COLS)
    )
    + sum(
        count("".join(lines[d-c][c] for c in range(min(d + 1, COLS))))
        for d in range(ROWS)
    )
    + sum(
        count("".join(lines[r][d-r] for r in range(ROWS - 1, max(-1, d - COLS), -1)))
        for d in range(ROWS, ROWS + COLS - 1)
    )
)
print(f"Part 1: {solution}")

count, ms = 0, {"M", "S"}
solution = sum(
    lines[r][c] == "A"
        and {lines[r-1][c-1], lines[r+1][c+1]} == ms
        and {lines[r-1][c+1], lines[r+1][c-1]} == ms
    for r in range(1, ROWS - 1)
    for c in range(1, COLS - 1)
)
print(f"Part 2: {solution}")
