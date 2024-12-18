print("Day 18")
EXAMPLE = False

file_name = f"2024/input/day_18{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    POSITIONS = tuple(
        tuple(map(int, reversed(line.split(",")))) for line in file
    )
LENGTH = 7 if EXAMPLE else 71
START, EXIT = (0, 0), (LENGTH - 1, LENGTH - 1)


def part_1(first):
    count, paths, visited = 0, {START}, set(POSITIONS[:first]) | {START}
    while paths:
        count += 1
        paths_new = set()
        for y, x in paths:
            for dy, dx in (0, 1), (1, 0), (0, -1), (-1, 0):
                y1, x1 = y + dy, x + dx
                p1 = y1, x1
                if 0 <= y1 < LENGTH and 0 <= x1 < LENGTH and p1 not in visited:
                    if p1 == EXIT:
                        return count
                    paths_new.add(p1)
                    visited.add(p1)
        paths = paths_new
    return None


print(f"Part 1: {part_1(12 if EXAMPLE else 1024)}")

left, right = 13 if EXAMPLE else 1025, len(POSITIONS) - 1
while left != right:
    mid = left + (right - left) // 2
    if part_1(mid) is None:
        right = mid - 1
    else:
        left = mid + 1
y, x = POSITIONS[left]
solution = f"{x},{y}"
print(f"Part 2: {solution}")
