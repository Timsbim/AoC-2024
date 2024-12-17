print("Day 17")
EXAMPLE = False

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
print(f"Part 1: {','.join(map(str, out))}")


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
print(f"Part 2: {min(candidates)}")
