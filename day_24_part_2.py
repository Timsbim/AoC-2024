from operator import and_, or_, xor
from textwrap import indent


print("Day 24")
EXAMPLE = False

file_name = f"2024/input/day_24{'_example' if EXAMPLE else ''}.txt"
with open(file_name, "r") as file:
    wires, gates = file.read().split("\n\n")
WIRES = {}
for wire in wires.splitlines():
    key, value = wire.split(": ")
    WIRES[key] = int(value)
GATES = []
for gate in gates.splitlines():
    a, op, b, c = gate.replace(" ->", "").split()
    for r in a, b, c:
        if r not in WIRES:
            WIRES[r] = None
    GATES.append([a, op, b, c])
Zs = tuple(sorted(wire for wire in WIRES if wire[0] == "z"))


"""
Here's my strategey for solving the puzzle. My assumption was that the system
is running the following algorithm to add x and y: Let

    x := x_n ... x_0
    y := y_n ... y_0

be two binary numbers with digits x_i/y_i in {0, 1}. z := x + y can be computed
by the following simple algrithm works (which can be easily shown by complete
induction :)):

    Start (n = 0):
        
        z_0 = x_0 ^ y_0
        c_0 = x_0 & y_0  <= the part that is carried over

    Recursion for n > 0:

        z_n =  (x_n ^ y_n) ^ c_n-1
        c_n = [(x_n ^ y_n) & c_n-1] | (x_n & y_n)

Or, to align it with the puzzle algorithm:

    Start (n = 0):

        c_0 = x_0 ^ y_0
        d_0 = 0
        z_0 = c_0

    Recursion for n > 0:

        a = d_n-1 & c_n-1
        b = x_n-1 & y_n-1
        c_n = x_n ^ y_n
        d_n = b | a
        z_n = d_n ^ b

To hone in on the wrong gates I've used the two functions:

 - run_and_show_error: it runs the system and shows which z's aren't compute as
                       expected
 - show_algorithm: shows the actual algorithm in a way that makes it relatively
                   easy to detect the deviations from the expected algorithm

As of now I don't have an implementation that detects the gate swaps ... work
in progress.
"""


def to_int(wires, c):
    ws = reversed(sorted(wire for wire in wires if wire[0] == c))
    return int("".join(str(wires[wire]) for wire in ws), 2)


Z = to_int(WIRES, "x") + to_int(WIRES, "y")
bits = reversed(bin(Z)[2:])
TARGET_Zs = {f"z{n:0>2}": int(bit) for n, bit in enumerate(bits)}

OPS = {"AND": and_, "OR": or_, "XOR": xor}


def step(wires, gates):
    for instruction in gates:
        a, op, b, c = instruction
        if (a := wires[a]) is not None and (b := wires[b]) is not None:
            wires[c] = OPS[op](a, b)
    return all(wires[z] is not None for z in Zs)


def run_and_show_errors(gates):
    print("Running algorithm:")
    wires = dict(WIRES)
    last = {wire for wire in wires if wire[0] in ("x", "y")}
    for n in range(1, 100):
        step(wires, GATES)
        news = {
            wire: value
            for wire, value in wires.items()
            if wire not in last and value is not None
        }
        wrongs = []
        for wire, value in news.items():
            if wire[0] == "z" and TARGET_Zs[wire] != value:
                wrongs.append((wire, value, TARGET_Zs[wire]))
        if wrongs:
            print(f" step {n}: wrong z-value(s):")
            for wire, value, target in wrongs:
                print(f"   - {wire} = {value} != {target}")
        last.update(news)
        if len(last) == len(wires):
            break


run_and_show_errors(GATES)


def show_algorithm(until=None):
    if until is None:
        until = len(Zs)
    fmt, short = "{: >3}: {} {} {} => {}", {"AND": "&", "OR": "|", "XOR": "^"}
    algorithm = {}
    for n, z in enumerate(Zs):
        layers, wires = [], [z]
        while wires:
            layer, wires_new = [], []
            for wire in wires:
                for i, (a, op, b, c) in enumerate(GATES):
                    if c == wire:
                        wires_new.extend((a, b))
                        layer.append((i, (a, op, b, c)))
            wires = wires_new
            layer = sorted(layer, key=lambda t: t[1][1])
            layers.extend(layer)
            if len(layers) > 4:
                break
        algorithm[z] = "\n".join(
            fmt.format(i, a, short[op], b, c)
            for i, (a, op, b, c) in reversed(layers)
        )
        print(f"{z}:")
        print(indent(algorithm[z], "     "))
        if n == until:
            return algorithm


show_algorithm()
