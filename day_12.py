from itertools import groupby
from operator import itemgetter


print("Day 12")
EXAMPLE = False

file_name = f"2024/input/day_12"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"
with open(file_name, "r") as file:
    plants = {}
    for r, row in enumerate(file):
        for c, plant in enumerate(row.rstrip()):
            plants.setdefault(plant, set()).add((r, c))


def plot_it(spots):
    while spots:
        p = spots.pop()
        plot, rim = {p}, {p}
        while rim:
            rim_new = set()
            for r, c in rim:
                for dr, dc in (0, 1), (1, 0), (0, -1), (-1, 0):
                    p = r + dr, c + dc
                    if p in spots:
                        plot.add(p)
                        spots.remove(p)
                        rim_new.add(p)
            rim = rim_new
        yield plot


plots = tuple(plot for spots in plants.values() for plot in plot_it(spots))


def holes(row):
    return sum(b - a > 1 for a, b in zip(row, row[1:]))


def fences(plot):
    rows = tuple(
        tuple(c for _, c in group)
        for _, group in groupby(sorted(plot), key=itemgetter(0))
    )
    
    row_0 = rows[0]
    if len(rows) == 1:
        return 2 * (len(row_0) + holes(row_0) + 1)
    
    count = len(row_0) + 2 * (holes(row_0) + 1)
    cols_0 = set(row_0)
    for i, row_1 in enumerate(rows[1:], 1):
        count += 2 * (holes(row_1) + 1)
        cols_1 = set(row_1)
        count += len(cols_0 ^ cols_1)
        row_0, cols_0 = row_1, cols_1
    
    return count + len(row_1)
    

print(f"Part 1: {sum(len(plot) * fences(plot) for plot in plots)}")


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


print(f"Part 2: {sum(len(plot) * sides(plot) for plot in plots)}")
