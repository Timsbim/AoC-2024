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
    rows = {}
    for r, c in plot:
        rows.setdefault(r, []).append(c)
    rows = tuple(sorted(rows[r]) for r in sorted(rows.keys()))
    
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
        rows, key_i, key_j = {}, itemgetter(i), itemgetter(j)
        for p in plot:
            rows.setdefault(key_i(p), []).append(key_j(p))
        rows = tuple(rows[r] for r in sorted(rows.keys()))

        row_0 = rows[0]
        if i == 0 and (len(rows) == 1 or all(len(row) == 1 for row in rows)):
            return 4
        
        count += holes(sorted(row_0)) + 1
        cols_0 = set(row_0)
        for i, row in enumerate(rows[1:], 1):
            cols_1 = set(row)
            c0, state = -2, True
            for c1 in sorted(cols_0 ^ cols_1):
                if c1 - c0 > 1 or (c1 in cols_1) != state:
                    count += 1
                    state = c1 in cols_1
                c0 = c1
            cols_0 = cols_1
        count += holes(sorted(row)) + 1

    return count


print(f"Part 2: {sum(len(plot) * sides(plot) for plot in plots)}")
