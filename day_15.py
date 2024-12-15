print("Day 15")
EXAMPLE = False

file_name = f"2024/input/day_15"
if EXAMPLE:
    file_name += "_example"
file_name += ".txt"


def read_input(file_name, part=1):
    with open(file_name, "r") as file:
        lines, moves = file.read().split("\n\n")
    if part == 2:
        repl = {".": "..", "@": "@.", "#": "##", "O": "[]"}
        lines = "".join(repl.get(char, char) for char in lines)
    lines, moves = lines.splitlines(), moves.replace("\n", "")
    rows, cols = len(lines), len(lines[0])
    grid = {}
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char == "@":
                start = r, c
                grid[r, c] = "."
            else:
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
    # d in ("v", "^2)
    for i in (range(r + 1, ROWS) if d == "v" else range(r - 1, -1, -1)):
        match GRID[i, c]:
            case "#": return r0, c0
            case ".":
                GRID[r, c], GRID[i, c] = ".", "O"
                return r, c


GRID, START, ROWS, COLS, MOVES = read_input(file_name)
r, c = START
for d in MOVES:
    r, c = step(r, c, d)
solution = sum(100 * r + c for (r, c), char in GRID.items() if char == "O")
print(f"Part 1: {solution}")


def next_boxes(d, box):
    r, c = box
    r += 1 if d == "v" else -1
    cols = c - 1, c, c + 1
    chars = tuple(GRID[r, c] for c in cols)
    if "#" in chars[1:]:
        return "#"
    return tuple((r, c) for c, char in zip(cols, chars) if char == "[")


def connected(d, box):
    connection, layer = {box}, {box}
    while layer:
        layer_new = set()
        for box in layer:
            boxes = next_boxes(d, box)
            if boxes == "#":
                return "#"
            layer_new.update(boxes)
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


GRID, START, ROWS, COLS, MOVES = read_input(file_name, part=2)
r, c = START
for d in MOVES:
    r, c = step(r, c, d)
solution = sum(100 * r + c for (r, c), char in GRID.items() if char == "[")
print(f"Part 2: {solution}")
