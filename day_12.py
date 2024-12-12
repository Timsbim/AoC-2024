from itertools import groupby
from operator import itemgetter


print("Day 12")
EXAMPLE = False

file_name = f"2024/input/day_12"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"
with open(file_name, "r") as file:
    garden = tuple(line.rstrip() for line in file)

ROWS, COLS = len(garden), len(garden[0])


def move(r, c):
    for dr, dc in (0, 1), (1, 0), (0, -1), (-1, 0):
        r1, c1 = r + dr, c + dc
        if 0 <= r1 < ROWS and 0 <= c1 < COLS:
            yield r1, c1


plots, visited = [], set()
for r0 in range(ROWS):
    for c0 in range(COLS):
        if (p := (r0, c0)) in visited:
            continue
        visited.add(p)
        plant = garden[r0][c0]
        plot, rim = {p}, {p}
        while rim:
            rim_new = set()
            for r, c in rim:
                for p in move(r, c):
                    if p not in visited and garden[p[0]][p[1]] == plant:
                        plot.add(p)
                        rim_new.add(p)
                        visited.add(p)
            rim = rim_new
        plots.append(plot)
plots = tuple(plots)


def holes(row):
    return sum(b - a > 1 for a, b in zip(row, row[1:]))


def fences(plot):
    rows = tuple(
        tuple(c for _, c in group)
        for _, group in groupby(sorted(plot), key=itemgetter(0))
    )
    
    row_0 = rows[0]
    if len(rows) == 1:
        return 2 * len(row_0) + 2 + 2 * holes(row_0)       
    
    count = len(row_0) + 2 * (holes(row_0) + 1)
    cols_0 = set(row_0)
    for i, row_1 in enumerate(rows[1:], 1):
        count += 2 * (holes(row_1) + 1)
        cols_1 = set(row_1)
        count += len(cols_0 ^ cols_1)
        row_0, cols_0 = row_1, cols_1
    
    return count + len(row_1)
    

solution = sum(len(plot) * fences(plot) for plot in plots)
print(f"Part 1: {solution}")


def sides(plot):
    count = 0
    for i, j in (0, 1), (1, 0):
        key_i, key_j = itemgetter(i), itemgetter(j)
        rows = tuple(
            tuple(map(key_j, grp))
            for _, grp in groupby(sorted(plot, key=itemgetter(i, j)), key_i)
        )    
        
        row_0 = rows[0]
        if len(rows) == 1:
            return 4 * (holes(row_0) + 1)
        
        count += holes(row_0) + 1
        cols_0 = set(row_0)
        for i, row in enumerate(rows[1:], 1):
            cols_1 = set(row)
            if len(diff := sorted(cols_0 ^ cols_1)) > 0:
                key = lambda c: c in cols_1
                part = [diff[0]]
                for c in diff[1:]:
                    if c > part[-1] + 1:
                        count += sum(1 for _, _ in groupby(part, key))
                        part = [c]
                    else:
                        part.append(c)
                count += sum(1 for _, _ in groupby(part, key))
            cols_0 = cols_1
        count += holes(rows[-1]) + 1

    return count


solution = sum(len(plot) * sides(plot) for plot in plots)
print(f"Part 2: {solution}")
