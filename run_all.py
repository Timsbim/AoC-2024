import re
from argparse import ArgumentParser
from collections import Counter
from functools import cache, cmp_to_key, partial
from itertools import combinations, groupby, product
from math import prod
from operator import add, mul
from time import perf_counter


parser = ArgumentParser()
parser.add_argument("-e", "--example", action="store_true")
parser.add_argument("-d", "--days", default="1-25")
args = parser.parse_args()

EXAMPLE = args.example

interval = r"(\d{1,2}|\d{1,2}-\d{1,2})"
if re.match(rf"{interval}(,{interval})*", args.days):
    days = set()
    for part in args.days.split(","):
        interval = tuple(map(int, part.split("-")))
        for n in interval:
            if n == 0 or 25 < n:
                parser.error(f"-d: wrong argument(s): {n}")
        start, stop = interval[0], interval[-1]
        if start != stop and stop < start:
            parser.error(f"-d: wrong argument(s): {start} > {stop}")
        days.update(range(start, stop + 1))
else:
    parser.error("-d: wrong format!")
selected_days = tuple(sorted(days))        


def day_1():
    print("Day 1:")

    file_name = f"2024/input/day_01{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        numbers = tuple(zip(*(map(int, line.split()) for line in file)))

    solution = sum(
        abs(n - m) for n, m in zip(sorted(numbers[0]), sorted(numbers[1]))
    )
    print(f"  - part 1: {solution}")

    counts2 = Counter(numbers[1])
    solution = sum(n * counts2.get(n, 0) for n in numbers[0])
    print(f"  - part 2: {solution}")


def day_2():
    print("Day 2:")

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
    print(f"  - part 1: {solution}")


    def is_safe_mod(report):
        for i in range(len(report)):
            report_mod = report[:i] + report[i+1:]
            if is_safe(report_mod):
                return True
        return False
 

    solution = sum(is_safe_mod(report) for report in reports)
    print(f"  - part 2: {solution}")


def day_3():
    print("Day 3:")

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
    print(f"  - part 1: {solution}")

    re_trim = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")
    solution, mul = 0, True
    for m in re_trim.finditer(memory):
        if m[0] == "do()":
            mul = True
        elif m[0] == "don't()":
            mul = False
        elif mul:
            solution += int(m[1]) * int(m[2])
    print(f"  - part 2: {solution}")


def day_4():
    print("Day 4:")

    file_name = f"2024/input/day_04{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        lines = [line.rstrip() for line in file]
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
    print(f"  - part 1: {solution}")

    count, ms = 0, {"M", "S"}
    solution = sum(
        lines[r][c] == "A"
            and {lines[r-1][c-1], lines[r+1][c+1]} == ms
            and {lines[r-1][c+1], lines[r+1][c-1]} == ms
        for r in range(1, ROWS - 1)
        for c in range(1, COLS - 1)
    )
    print(f"  - part 2: {solution}")


def day_5():
    print("Day 5:")

    file_name = f"2024/input/day_05{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        orderings = set()
        while "|" in (line := next(file)):
            orderings.add(tuple(map(int, line.split("|"))))
        updates = tuple(tuple(map(int, line.split(","))) for line in file)


    def is_correct(update):
        for i, n in enumerate(update[:-1]):
            for m in update[i+1:]:
                if (n, m) not in orderings:
                    return False
        return True


    solution = sum(
        update[len(update) // 2] for update in updates if is_correct(update)
    )
    print(f"  - part 1: {solution}")

    def cmp(a, b): return 1 if (a, b) in orderings else -1

    key = cmp_to_key(cmp)
    solution = sum(
        sorted(update, key=key)[len(update) // 2]
        for update in updates
        if not is_correct(update)
    )
    print(f"  - part 2: {solution}")


def day_6():
    print(f"Day 6")

    DIRECTION = dict(zip(">v<^", range(4)))
    DELTA = (0, 1), (1, 0), (0, -1), (-1, 0)

    file_name = f"2024/input/day_06{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        grid = tuple(line.rstrip() for line in file)
    ROWS, COLS = len(grid), len(grid[0])
    obstacles = set()
    for r, line in enumerate(grid):
        for c, char in enumerate(line):
            if char == ".": continue
            if char == "#":
                obstacles.add((r, c))
            else:
                start, direction = (r, c), DIRECTION[char]

    visited, (r, c), d = {start}, start, direction
    while True:
        (dr, dc), d1 = DELTA[d], d
        while 0 <= (r1 := r + dr) < ROWS and 0 <= (c1 := c + dc) < COLS:
            if (r1, c1) in obstacles:
                d1 = (d + 1) % 4
                break
            r, c = r1, c1
            visited.add((r, c))
        if d1 == d: break
        d = d1
    print(f"  - part 1: {len(visited)}")

    count = 0
    for position in visited - {start}:
        obstacles_mod = obstacles | {position}
        (r, c), d = start, direction
        visited = {(r, c, d)}
        while True:
            (dr, dc), d1 = DELTA[d], d
            while 0 <= (r1 := r + dr) < ROWS and 0 <= (c1 := c + dc) < COLS:
                if (r1, c1) in obstacles_mod:
                    d1 = (d + 1) % 4
                    break
                r, c = r1, c1
            if d1 == d: break
            d = d1
            if (r, c, d) in visited:
                count += 1
                break
            visited.add((r, c, d))
    print(f"  - part 2: {count}")


def day_7():
    print("Day 7:")

    file_name = f"2024/input/day_07{'_example' if EXAMPLE else ''}.txt"
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
    print(f"  - part 1: {solution}")

    def concat(n, m): return int(f"{n}{m}")
    check = partial(solve, (add, mul, concat))
    solution = sum(test for test, numbers in equations if check(test, numbers))
    print(f"  - part 2: {solution}")


def day_8():
    print("Day 8:")

    file_name = f"2024/input/day_08{'_example' if EXAMPLE else ''}.txt"
    antennas = {}
    with open(file_name, "r") as file:
        lines = [line.rstrip() for line in file]
    ROWS, COLS = len(lines), len(lines[0])
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char != ".":
                antennas.setdefault(char, []).append((r, c))

    antinodes = set()
    for positions in antennas.values():
        for (r1, c1), (r2, c2) in combinations(positions, 2):
            for r, c in (2 * r1 - r2, 2 * c1 - c2), (2 * r2 - r1, 2 * c2 - c1):
                if 0 <= r < ROWS and 0 <= c < COLS:
                    antinodes.add((r, c))
    solution = len(antinodes)
    print(f"  - part 1: {solution}")

    antinodes = set()
    for positions in antennas.values():
        for (r1, c1), (r2, c2) in combinations(positions, 2):
            for r, c, dr, dc in (r1, c1, r1 - r2, c1 - c2), (r2, c2, r2 - r1, c2 - c1):
                while 0 <= r < ROWS and 0 <= c < COLS:
                    antinodes.add((r, c))
                    r, c = r + dr, c + dc
    solution = len(antinodes)
    print(f"  - part 2: {solution}")


def day_9():
    print("Day 9:")

    if EXAMPLE:
        disk_map = "2333133121414131402"
    else:
        with open("2024/input/day_09.txt", "r") as file:
            disk_map = file.read().rstrip()


    def checksum(disk):
        s = 0
        for i, n in enumerate(disk):
            if n != ".":
                s += i * n
        return s


    ID, files, occupied, free = -1, [], [], []
    for i, n in enumerate(disk_map):
        container, item = (free, ".") if i % 2 else (occupied, ID := ID + 1)
        l, n, = len(files), int(n)
        container.extend(range(l, l + n))
        files.extend(item for _ in range(n))
    for i, j in zip(free, reversed(occupied)):
        if j < i:
            break
        files[i], files[j] = files[j], "."
    print(f"  - part 1: {checksum(files)}")

    ID, files, occupied, free = -1, [], {}, {}
    for i, n in enumerate(disk_map):
        l, n, = len(files), int(n)
        container, key, item = (free, l, ".") if i % 2 else (occupied, ID := ID + 1, ID)
        container[key] = range(l, l + n)
        files.extend(item for _ in range(n))
    for ID, idxso in reversed(occupied.items()):
        i, l, found = idxso.start, len(idxso), False
        for j, idxsf in free.items():
            if i <= idxsf.start:
                break
            if l <= len(idxsf):
                found = True
                break
        if found:
            for k, l in zip(idxsf, idxso):
                files[k], files[l] = ID, "."
            if len(idxso) < len(idxsf):
                free[j] = range(idxsf.start + len(idxso), idxsf.stop)
            else:
                del free[j]
    print(f"  - part 2: {checksum(files)}")


def day_10():
    print("Day 10:")

    file_name = f"2024/input/day_10{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        topos = {
            (r, c): n
            for r, line in enumerate(file)
            for c, n in enumerate(map(int, line.rstrip()))
        }

    score = count = 0
    for (r0, c0), n in topos.items():
        if n: continue
        heads = [(r0, c0)]
        for n in range(1, 10):
            heads_new = []
            for r, c in heads:
                for dr, dc in (0, 1), (1, 0), (0, -1), (-1, 0):
                    if topos.get((r1 := r + dr, c1 := c + dc), -1) == n:
                        heads_new.append((r1, c1))
            heads = heads_new
        score, count = score + len(set(heads)), count + len(heads)

    print(f"  - part 1: {score}")
    print(f"  - part 2: {count}")


def day_11():
    print("Day 11:")

    file_name = f"2024/input/day_11{'_example' if EXAMPLE else ''}.txt"
    with open("2024/input/day_11.txt", "r") as file:
        arrangement = tuple(file.read().split())


    @cache
    def blink(stone):
        if stone ==  "0":
            return ("1",)
        if len(stone) % 2:
            return (str(int(stone) * 2024),)
        m = len(stone) // 2
        return stone[:m], str(int(stone[m:]))


    def count(counts, steps):
        for _ in range(steps):
            counts_new = Counter()
            for stone, n in counts.items():
                for stone in blink(stone):
                    counts_new[stone] += n
            counts = counts_new
        return counts


    print(f"  - part 1: {(counts := count(Counter(arrangement), 25)).total()}")
    print(f"  - part 2: {count(counts, 50).total()}")


def day_12():
    print("Day 12:")

    file_name = f"2024/input/day_12{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        plants = {}
        for r, row in enumerate(file):
            for c, plant in enumerate(row.rstrip()):
                plants.setdefault(plant, set()).add((r, c))

    ds = (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)
    count_1 = count_2 = 0
    for p, spots in plants.items():
        rest = set(spots)
        while rest:
            s = rest.pop()
            count = fences = sides = 0
            rim = {s}
            while rim:
                count += len(rim)
                rim_new = set()
                for r, c in rim:
                    for i in range(0, 7, 2):
                        dr, dc = ds[i]
                        s = r + dr, c + dc
                        if s in rest:
                            rest.remove(s)
                            rim_new.add(s)
                        if s not in spots:
                            fences += 1
                            (dr2, dc2), (dr1, dc1) = ds[i-2], ds[i-1]
                            b2 = (r + dr2, c + dc2) not in spots
                            b1 = (r + dr1, c + dc1) not in spots
                            if b2 or not (b2 or b1):
                                sides += 1                             
                rim = rim_new
            count_1 += count * fences
            count_2 += count * sides
    
    print(f"  - part 1: {count_1}")
    print(f"  - part 2: {count_2}")


def day_13():
    print("Day 13:")

    file_name = f"2024/input/day_13{'_example' if EXAMPLE else ''}.txt"
    re_xy = re.compile(r"X(?:\+|=)(\d+), Y(?:\+|=)(\d+)")
    with open(file_name, "r") as file:
        blocks = file.read().split("\n\n")
    machines = []
    for block in blocks:
        machines.append(tuple(
            tuple(map(int, re_xy.search(line).groups()))
            for line in block.splitlines()
        ))
    machines = tuple(machines)


    def det(x, y):
        return x[0] * y[1] - x[1] * y[0]


    def costs(a, b, p):
        if (d := det(a, b)) != 0:
            da, db = det(p, b), det(a, p)
            na, nb = da // d, db // d
            if all(na * a[i] + nb * b[i] == p[i] for i in (0, 1)):
                return na * 3 + nb

        n = None
        if all(a[i] != 0 for i in (0, 1)):
            n0, n1 = (p[i] // a[i] for i in (0, 1))
            if n0 == n1 and all(n0 * a[i] == p[i] for i in (0, 1)):
                n = n0 * 3
        if all(b[i] != 0 for i in (0, 1)):
            n0, n1 = (p[i] // b[i] for i in (0, 1))
            if n0 == n1 and all(n0 * b[i] == p[i] for i in (0, 1)):
                n = min(n, n0) if n is not None else n0    
    
        return n if n is not None else 0


    print(f"  - part 1: {sum(costs(a, b, p) for a, b, p in machines)}")
    s = 10_000_000_000_000
    print(f"  - part 2: {sum(costs(a, b, (p[0] + s, p[1] + s)) for a, b, p in machines)}")


def day_14():
    print("Day 14:")

    positions, velocities = [], []
    file_name = f"2024/input/day_14{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        for line in file:
            position, velocity = line.split()
            x, y = map(int, position[2:].split(","))
            positions.append((y, x))
            vx, vy = map(int, velocity[2:].split(","))
            velocities.append((vy, vx))
    POSITIONS, VELOCITIES = tuple(positions), tuple(velocities)
    ROWS, COLS = (7, 11) if EXAMPLE else (103, 101)
    ROWS_M, COLS_M = ROWS // 2, COLS // 2


    def safety_factor(positions):
        quadrants = {(0, 0): 0, (0, 1): 0, (1, 0): 0, (1, 1): 0}
        for y, x in positions:
            if y != ROWS_M and x != COLS_M:
                quadrants[int(y < ROWS_M), int(x < COLS_M)] += 1    
        return prod(quadrants.values())


    solution = safety_factor(
        ((py + 100 * vy) % ROWS, (px + 100 * vx) % COLS)
        for (py, px), (vy, vx) in zip(POSITIONS, VELOCITIES)
    )
    print(f"  - part 1: {solution}")

    minimum, positions = float("inf"), POSITIONS
    for second in range(1, 10404):
        positions = tuple(
            ((py + vy) % ROWS, (px + vx) % COLS)
            for (py, px), (vy, vx) in zip(positions, VELOCITIES)
        )
        if (factor := safety_factor(positions)) < minimum:
            minimum, second_min = factor, second
    print(f"  - part 2: {second_min}")


def day_15():
    print("Day 15:")

    FILE_NAME = f"2024/input/day_15{'_example' if EXAMPLE else ''}.txt"


    def read_input(part=1):
        with open(FILE_NAME, "r") as file:
            layout, moves = file.read().split("\n\n")
        if part == 2:
            repl = {".": "..", "@": "@.", "#": "##", "O": "[]"}
            layout = "".join(repl.get(char, char) for char in layout)
        lines, moves = layout.splitlines(), moves.replace("\n", "")
        rows, cols = len(lines), len(lines[0])
        grid = {}
        for r, line in enumerate(lines):
            for c, char in enumerate(line):
                if char == "@":
                    start, char = (r, c), "."
                grid[r, c] = char
        return grid, start, rows, cols, moves


    DELTA = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}


    def step(r0, c0, d):
        dr, dc = DELTA[d]
        match GRID[r := r0 + dr, c := c0 + dc]:
            case "#": return r0, c0
            case ".": return r, c
        # Box: "O"
        if d in (">", "<"):
            for i in (range(c + 1, COLS) if d == ">" else range(c - 1, -1, -1)):
                match GRID[r, i]:
                    case "#": return r0, c0
                    case ".":
                        GRID[r, c], GRID[r, i] = ".", "O"
                        return r, c
        # d in ("v", "^")
        for i in (range(r + 1, ROWS) if d == "v" else range(r - 1, -1, -1)):
            match GRID[i, c]:
                case "#": return r0, c0
                case ".":
                    GRID[r, c], GRID[i, c] = ".", "O"
                    return r, c


    GRID, START, ROWS, COLS, MOVES = read_input()
    r, c = START
    for d in MOVES:
        r, c = step(r, c, d)
    solution = sum(100 * r + c for (r, c), char in GRID.items() if char == "O")
    print(f"  - part 1: {solution}")


    def connected(d, box):
        dr = 1 if d == "v" else -1
        connection, layer = {box}, {box}
        while layer:
            layer_new = set()
            for r, c in layer:
                r += dr
                for dc in -1, 0, 1:
                    char = GRID[r, c1 := c + dc]
                    if dc >= 0 and char == "#":
                        return "#"
                    if char == "[":
                        layer_new.add((r, c1))
            layer = layer_new
            connection.update(layer)
        return tuple(connection)


    def step(r0, c0, d):
        dr, dc = DELTA[d]
        match char := GRID[r := r0 + dr, c := c0 + dc]:
            case "#": return r0, c0
            case ".": return r, c
        # Box: "[]"
        if d in (">", "<"):
            for i in (range(c + 1, COLS) if d == ">" else range(c - 1, -1, -1)):
                match GRID[r, i]:
                    case "#": return r0, c0
                    case ".":
                        dc = -1 if d == ">" else 1
                        for j in (range(i, c, -1) if d == ">" else range(i, c)):
                            GRID[r, j] = GRID[r, j + dc]
                        GRID[r, c] = "."
                        return r, c
        # d in ("v", "^")
        connection = connected(d, (r, c) if char == "[" else (r, c - 1))
        if connection == "#":
            return r0, c0
        base, dr = (r, c), 1 if d == "v" else -1
        for r, c in connection:
            GRID[r, c] = GRID[r, c + 1] = "."
        for r, c in connection:
            GRID[r + dr, c], GRID[r + dr, c + 1] = "[", "]"
        return base


    GRID, START, ROWS, COLS, MOVES = read_input(part=2)
    r, c = START
    for d in MOVES:
        r, c = step(r, c, d)
    solution = sum(100 * r + c for (r, c), char in GRID.items() if char == "[")
    print(f"  - part 2: {solution}")


def day_16():
    print("Day 16:")

    grid = {}
    file_name = f"2024/input/day_16{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        for r, line in enumerate(file):
            for c, char in enumerate(line.rstrip()):
                if char != "#":
                    grid.setdefault(char, set()).add((r, c))
    start, end = grid["S"].pop(), grid["E"].pop()
    grid = grid["."] | {start, end}

    DELTA = (0, 1), (1, 0), (0, -1), (-1, 0)
    INF = float("inf")

    minimum, paths, dists = INF, [(start, 0, 0)], {(start, 0): 0}
    while paths:
        paths_new = []
        for (r, c), d, cost in paths:
            for d, add in (d, 1), ((d - 1) % 4, 1_001), ((d + 1) % 4, 1_001):
                if (cost_new := cost + add) >= minimum: continue
                dr, dc = DELTA[d]
                if (((p := (r + dr, c + dc)) in grid
                        and cost_new < dists.get((p, d), INF))):
                    dists[p, d] = cost_new
                    if p == end:
                        minimum = cost_new
                    else:
                        paths_new.append((p, d, cost_new))
        paths = paths_new
    print(f"  - part 1: {minimum}")

    seats, paths = {end}, [((start,), 0, 0)]
    while paths:
        path, d, cost = paths.pop()
        r, c = path[-1]
        for d, add in (d, 1), ((d - 1) % 4, 1_001), ((d + 1) % 4, 1_001):
            if (cost_new := cost + add) > minimum: continue
            dr, dc = DELTA[d]
            if (p := (r + dr, c + dc)) in grid and cost_new == dists[p, d]:
                if p == end:
                    seats.update(path)
                else:
                    paths.append((path + (p,), d, cost_new))
    print(f"  - part 2: {len(seats)}")


def day_17():
    print("Day 17:")

    file_name = f"2024/input/day_17{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        registers, program = file.read().split("\n\n")
    initial_state = {}
    for register in registers.splitlines():
        _, reg, val = register.split()
        initial_state[reg[0]] = int(val)
    PROGRAM = tuple(map(int, program.split()[1].split(",")))
    LENGTH = len(PROGRAM)

    REGS = {4: "A", 5: "B", 6: "C"}


    def step(state, out, i):
        op = PROGRAM[i + 1]
        combo = op if op < 4 else state[REGS[op]]
        match PROGRAM[i]:
            case 0: state["A"] = state["A"] // (2 ** combo)
            case 1: state["B"] = state["B"] ^ op
            case 2: state["B"] = combo % 8
            case 3: return i + 2 if state["A"] == 0 else op
            case 4: state["B"] = state["B"] ^ state["C"]
            case 5: out.append(combo % 8)
            case 6: state["B"] = state["A"] // (2 ** combo)  
            case 7: state["C"] = state["A"] // (2 ** combo)             

        return i + 2


    state, out, i = initial_state, [], 0
    while 0 <= (i := step(state, out, i)) < LENGTH:
        pass   
    print(f"  - part 1: {','.join(map(str, out))}")


    def one_out(A):
        out, state, i = [], {"A": A, "B": 0, "C": 0}, 0
        while 0 <= (i := step(state, out, i)) < LENGTH:
            if out:
                return out[0]
    

    candidates = [0]
    for p in PROGRAM[::-1]:
        candidates_new = []
        for c in candidates:
            for A in range(c * 8, c * 8 + 8):
                if one_out(A) == p:
                    candidates_new.append(A)
        candidates = candidates_new
    print(f"  - part 2: {min(candidates)}")


def day_18():
    print("Day 18:")

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


    print(f"  - part 1: {part_1(12 if EXAMPLE else 1024)}")

    left, right = 13 if EXAMPLE else 1025, len(POSITIONS) - 1
    while left != right:
        mid = left + (right - left) // 2
        if part_1(mid) is None:
            right = mid - 1
        else:
            left = mid + 1
    y, x = POSITIONS[left]
    solution = f"{x},{y}"
    print(f"  - part 2: {solution}")


def day_19():
    print("Day 19:")

    file_name = f"2024/input/day_19{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        patterns, designs =  file.read().split("\n\n")
    PATTERNS = set(patterns.split(", "))


    @cache
    def accounting(design):
        return (1 if design in PATTERNS else 0) + sum(
            accounting(design[len(pattern):])
            for pattern in PATTERNS
            if design.startswith(pattern)
        )


    counts = [*map(accounting, designs.splitlines())]
    print(f"  - part 1: {sum(map(bool, counts))}")
    print(f"  - part 2: {sum(counts)}")


def day_20():
    print("Day 20:")

    file_name = f"2024/input/day_20{'_example' if EXAMPLE else ''}.txt"
    GRID = set()
    with open(file_name, "r") as file:
        for r, line in enumerate(file):
            for c, char in enumerate(line):
                if char == "#": continue
                if char == "S":
                    START = r, c
                elif char == "E":
                    END = r, c
                GRID.add((r, c))
    THRESHOLD = 50 if EXAMPLE else 100

    path = [None, START]
    while path[-1] != END:
        r, c = path[-1]
        for dr, dc in (0, 1), (1, 0), (-1, 0), (0, -1):
            p = r + dr, c + dc
            if p != path[-2] and p in GRID:
                path.append(p)
                break
    path = {p: n for n, p in enumerate(path[1:])}

    dps = {}
    for dist in range(2, 21):
        rim = dps[dist] = [(dist, 0)]
        for dr in range(1, dist):
            rim.append((dr, c1 := dist - dr))
            rim.append((-dr, c1))
        rim.append((0, dist))

    count_1 = count_2 = 0
    for (r0, c0), t0 in path.items():
        for dist, rim in dps.items():
            for dr, dc in rim:
                p1 = r0 + dr, c0 + dc
                if p1 in path and abs(path[p1] - t0) - dist >= THRESHOLD:
                    if dist == 2:
                        count_1 += 1
                    else:
                        count_2 += 1                        
    count_2 += count_1

    print(f"  - part 1: {count_1}")
    print(f"  - part 2: {count_2}")


def day_21():
    print("Day 21:")

    file_name = f"2024/input/day_21{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        CODES = tuple(file.read().splitlines())
    if EXAMPLE:
        pprint(CODES)

    DELTA = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    REV = dict(zip("^v<>A", "v^><A"))

    NUM = {
        (r, c): char
        for r, line in enumerate("789|456|123| 0A".split("|"))
        for c, char in enumerate(line)
        if char != " "
    }
    NUMPAD = dict.fromkeys(zip("0123456789A", "0123456789A"), ("",))
    for (r0, c0), (r1, c1) in combinations(NUM, 2):
        k0, k1 = NUM[r0, c0], NUM[r1, c1]
        ver = "v" * dr if (dr := r1 - r0) >= 0 else "^" * abs(dr)
        hor = ">" * dc if (dc := c1 - c0) >= 0 else "<" * abs(dc)
        NUMPAD[k0, k1] = (hor + ver,)
        if (c0 != 0 or r1 != 3) and (dr != 0 and dc != 0):
            NUMPAD[k0, k1] += (ver + hor,)
        NUMPAD[k1, k0] = tuple(
            "".join(REV[c] for c in seq[::-1]) for seq in NUMPAD[k0, k1]
        )


    # Why not just do this part manually :)
    DIR = {
        (r, c): char
        for r, line in enumerate(" ^A|<v>".split("|"))
        for c, char in enumerate(line)
        if char != " "
    }
    DIRPAD = dict.fromkeys(zip("^v<>A", "^v<>A"), ("",))
    for (r0, c0), (r1, c1) in combinations(DIR, 2):
        k0, k1 = DIR[r0, c0], DIR[r1, c1]
        ver = "v" * dr if (dr := r1 - r0) >= 0 else "^" * abs(dr)
        hor = ">" * dc if (dc := c1 - c0) >= 0 else "<" * abs(dc)
        DIRPAD[k0, k1] = (ver + hor,)
        if (r1 != 1 or c1 != 0) and abs(dr) == 1 and abs(dc) == 1:
            DIRPAD[k0, k1] += (hor + ver,)
        DIRPAD[k1, k0] = tuple(
            "".join(REV[c] for c in seq[::-1]) for seq in DIRPAD[k0, k1]
        )


    @cache
    def length(path, n):
        if n == 0:
            return len(path)
        count = 0
        for As, group in groupby(path, key=lambda char: char == "A"):
            path = "".join(group)
            if As:
                count += len(path) - 1
                continue
            paths = product(*map(DIRPAD.get, zip(f"A{path}", f"{path}A")))
            paths = ("A".join(path) + "A" for path in paths)
            count += min(length(path, n-1) for path in paths)
        return count


    def complexity(code, n=2):
        paths = product(*map(NUMPAD.get, zip(f"A{code}", code)))
        paths = ("A".join(path) + "A" for path in paths)
        return int(code.replace("A", "")) * min(length(path, n) for path in paths)


    print(f"  - part 1: {sum(map(complexity, CODES))}")
    print(f"  - part 2: {sum(complexity(code, n=25) for code in CODES)}")


def day_22():
    print("Day 22:")

    file_name = f"2024/input/day_22{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        SECRETS = tuple(int(line.rstrip()) for line in file)
    PRUNE = 16777216
    

    def next_secret(secret):
        secret = ((secret * 64) ^ secret) % PRUNE
        secret = ((secret // 32) ^ secret) % PRUNE
        return ((secret * 2048) ^ secret) % PRUNE


    solution_1, bananas = 0, {}
    for secret in SECRETS:
        price, prices, changes = secret % 10, [], []
        for _ in range(2_000):
            secret = next_secret(secret)
            price_new = secret % 10
            changes.append(price_new - price)
            prices.append(price_new)
            price = price_new
        solution_1 += secret
        candidates = set()
        for i in range(3, 2_000):
            sequence = tuple(changes[i-3:i+1])
            if sequence in candidates or sum(sequence) < 0: continue
            candidates.add(sequence)
            bananas[sequence] = bananas.get(sequence, 0) + prices[i]    

    print(f"  - part 1:", solution_1)
    print(f"  - part 2:", max(bananas.values()))


def day_23():
    print("Day 23:")

    file_name = f"2024/input/day_23{'_example' if EXAMPLE else ''}.txt"
    with open(file_name, "r") as file:
        EDGES = tuple(tuple(line.rstrip().split("-")) for line in file)

    nodes = {i: n for i, n in enumerate(sorted({n for e in EDGES for n in e}))}
    numbers = {n: i for i, n in nodes.items()}
    graph = {n: [] for n in nodes}
    for n0, n1 in sorted((numbers[n0], numbers[n1]) for n0, n1 in EDGES):
        if n0 < n1:
            graph[n0].append(n1)
        else:
            graph[n1].append(n0)
    num_nodes, neighbours = len(graph), {n: set(ns) for n, ns in graph.items()}
    cliques, length = [(n0, n1) for n0 in graph for n1 in graph[n0]], 2
    while cliques:
        cliques_new = []
        for clique in cliques:
            for n1 in range(clique[-1] + 1, num_nodes):
                if all(n1 in neighbours[n0] for n0 in clique):
                    cliques_new.append(clique + (n1,))
        if len(cliques_new) == 0:
            break
        cliques = cliques_new
        length += 1
        if length == 3:
            solution_1 = sum(
                any(nodes[n].startswith("t") for n in c) for c in cliques
            )

    print(f"  - part 1:", solution_1)
    print(f"  - part 2:", ",".join(map(nodes.get, cliques[0])))


days = {
    1: day_1,
    2: day_2,
    3: day_3,
    4: day_4,
    5: day_5,
    6: day_6,
    7: day_7,
    8: day_8,
    9: day_9,
    10: day_10,
    11: day_11,
    12: day_12,
    13: day_13,
    14: day_14,
    15: day_15,
    16: day_16,
    17: day_17,
    18: day_18,
    19: day_19,
    20: day_20,
    21: day_21,
    22: day_22,
    23: day_23
}


if __name__ == "__main__":


    total_ms = 0
    for day in selected_days:
        if day not in days: continue
        func = days[day]
        start = perf_counter()
        func()
        end = perf_counter()
        ms = (end - start) * 1_000
        print(f"  => run time: {ms:.0f} ms\n")
        total_ms += ms
    print(f"\n=> total run time: {total_ms:.0f} ms\n")
