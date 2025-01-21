
def AND(wire_1, wire_2):
    return wire_1 & wire_2

def OR(wire_1, wire_2):
    return wire_1 | wire_2

def XOR(wire_1, wire_2):
    return wire_1 ^ wire_2

def apply_operation(wire_1, operation, wire_2):
    return globals()[operation](int(wire_1), int(wire_2))

if __name__ == '__main__':
    wire_states = {}
    with open('input.in') as f:
        for line in f:
            if line == '\n':
                break
            wire, value = line.strip().split(': ')
            wire_states[wire] = value
        remaining_operations = [(comp[0], comp[1], comp[2], comp[4]) for comp in [line.strip().split(' ') for line in f]]

    while remaining_operations:
        for i in reversed(range(len(remaining_operations))):
            wire_1, operation, wire_2, output_wire = remaining_operations[i]
            if wire_1 in wire_states and wire_2 in wire_states:
                wire_states[output_wire] = apply_operation(wire_states[wire_1], operation, wire_states[wire_2])
                remaining_operations.pop(i)

    output = ''.join([str(wire_states[z_wire]) for z_wire in sorted([key for key in wire_states if key.startswith('z')], reverse=True)])
    print(int(output, 2))
