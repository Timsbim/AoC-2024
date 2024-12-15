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
        lines = (
            lines.replace(".", "..") .replace("@", "@.")
                 .replace("#", "##") .replace("O", "[]")
        )
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


DIRECTION = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}


def step(r0, c0, d):
    dr, dc = DIRECTION[d]
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
    if d in ("v", "^"):
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
    (r, c0, c1) = box
    r += 1 if d == "v" else -1
    cols = c0 - 1, c0, c1
    chars = tuple(GRID[r, c] for c in cols)
    if "#" in chars[1:]:
        return "#"
    return tuple((r, c, c + 1) for c, char in zip(cols, chars) if char == "[")


def get_connection(d, box):
    connection, layer = {box}, {box}
    while layer:
        layer_new = set()
        for box in layer:
            boxes = next_boxes(d, box)
            if boxes == "#":
                return "#"
            layer_new.update(boxes)
        if layer_new:
            connection |= layer_new
        layer = layer_new
    return tuple(connection)


def step(r0, c0, d):
    dr, dc = DIRECTION[d]
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
    if d in ("v", "^"):
        base = r, c
        box = (r, c, c + 1) if char == "[" else (r, c - 1, c)
        connection = get_connection(d, box)
        if connection != "#":
            dr = 1 if d == "v" else -1
            for r, c0, c1 in connection:
                GRID[r, c0] = GRID[r, c1] = "."
            for r, c0, c1 in connection:
                GRID[r + dr, c0], GRID[r + dr, c1] = "[", "]"
            return base
        return r0, c0


GRID, START, ROWS, COLS, MOVES = read_input(file_name, part=2)
r, c = START
for d in MOVES:
    r, c = step(r, c, d)
solution = sum(100 * r + c for (r, c), char in GRID.items() if char == "[")
print(f"Part 2: {solution}")
