from operator import and_, or_, xor


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
    GATES.append((a, op, b, c))
GATES = tuple(GATES)
Zs = tuple(sorted(wire for wire in WIRES if wire[0] == "z"))


def to_int(wires, c):
    ws = reversed(sorted(wire for wire in wires if wire[0] == c))
    return int("".join(str(wires[wire]) for wire in ws), 2)

OPS = {"AND": and_, "OR": or_, "XOR": xor}


def run(wires, gates):
    stop = False
    while not stop:
        for gate in gates:
            a, op, b, c = gate
            if (a := wires[a]) is not None and (b := wires[b]) is not None:
                wires[c] = OPS[op](a, b)
        stop = all(wires[z] is not None for z in Zs)


wires, gates = dict(WIRES), GATES
run(wires, gates)
print("Part 1:", to_int(wires, "z"))

# So far my part 2 solution is partly manually
if not EXAMPLE:
    print("Part 2:", "gsd,kth,qnf,tbt,vpm,z12,z26,z32")
