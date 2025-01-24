class Gate:
    def __init__(self, name, value=None, logic=None):
        self.name = name
        self.value = value
        self.logic = logic
        self.outputs = []

        if logic is not None:
            self.input_a = logic[0]
            self.input_b = logic[1]
            self.operation = logic[2]
        
    def is_z(self):
        return self.name[0] == 'z'
    
    def is_input(self):
        return self.name[0] in ['x', 'y']
    
    def __repr__(self):
        logic_string = ''
        if not self.is_input():
            input_a = f"{self.input_a.name} - {self.input_a.value}" if self.input_a.is_input() else f"{self.input_a.name} - {self.input_a.operation}"
            input_b = f"{self.input_b.name} - {self.input_b.value}" if self.input_b.is_input() else f"{self.input_b.name} - {self.input_b.operation}"
            logic_string =  f': ({input_a}) {self.operation} ({input_b}) '
        output_string = '' if self.is_z() else '-> (' + ', '.join([(output.name + ' ' + output.operation) for output in self.outputs]) + ')'
        return self.name + ' ' + str(self.value) + logic_string + output_string

def AND(wire_1, wire_2): return wire_1 & wire_2
def OR(wire_1, wire_2): return wire_1 | wire_2
def XOR(wire_1, wire_2): return wire_1 ^ wire_2

def apply_operation(wire_1, operation, wire_2):
    return globals()[operation](int(wire_1), int(wire_2))

def traverse_circuit(circuit, wire):
    if circuit[wire].value is not None:
        return circuit[wire].value
    else:
        circuit[wire].value = apply_operation(
            traverse_circuit(circuit, circuit[wire].input_a.name),
            circuit[wire].operation,
            traverse_circuit(circuit, circuit[wire].input_b.name)
        )
        return circuit[wire].value

if __name__ == '__main__':
    circuit = {}
    operations = []
    with open('input.in') as f:
        for line in f:
            if line == '\n':
                break
            wire, value = line.strip().split(': ')
            circuit[wire] = Gate(wire, value=value)

        for line in f:
            wire_a, operation, wire_b, _, output_wire = line.strip().split(' ')
            if wire_a not in circuit:
                circuit[wire_a] = Gate(wire_a)
            if wire_b not in circuit:
                circuit[wire_b] = Gate(wire_b)
            circuit[output_wire] = Gate(output_wire, logic=(circuit[wire_a], circuit[wire_b], operation))
            circuit[wire_a].outputs.append(circuit[output_wire])
            circuit[wire_b].outputs.append(circuit[output_wire])
            
            for wire in circuit:
                if circuit[wire].logic is not None:
                    if circuit[wire].input_a.name == output_wire:
                        circuit[wire].input_a = circuit[output_wire]
                        circuit[output_wire].outputs.append(circuit[wire])
                    if circuit[wire].input_b.name == output_wire:
                        circuit[wire].input_b = circuit[output_wire]
                        circuit[output_wire].outputs.append(circuit[wire])

    # Part 1
    z_values = ''.join([str(traverse_circuit(circuit, z_wire)) for z_wire in sorted([key for key in circuit if key.startswith('z')], reverse=True)])
    print('Z:', int(z_values, 2))

    # Part 2
    faulty_gates = set()
    print("if it is a z gate, the operation must be XOR unless it's z45")
    for wire in circuit:
        if circuit[wire].is_z():
            if circuit[wire].operation != 'XOR' and wire != 'z45':
                print(circuit[wire])
                faulty_gates.add(wire)

    print("if it is not a z gate, and inputs are not x and y, it can't be an XOR gate")
    for wire in circuit:
        if not circuit[wire].is_input() and not circuit[wire].is_z():
            if not circuit[wire].input_a.is_input() and not circuit[wire].input_b.is_input():
                if circuit[wire].operation == 'XOR':
                    print(circuit[wire])
                    faulty_gates.add(wire)

    print("if the operation is XOR, and the inputs are x and y, there must be an XOR gate after it")
    for wire in circuit:
        if not circuit[wire].is_input() and circuit[wire].operation == 'XOR':
            if circuit[wire].input_a.is_input() and circuit[wire].input_b.is_input():
                has_xor = False
                for output in circuit[wire].outputs:
                    if output.operation == 'XOR':
                        has_xor = True
                        break
                if not has_xor and wire != 'z00':
                    print(circuit[wire])
                    faulty_gates.add(wire)

    print("if it is an AND gate, there must be an OR gate after it")
    for wire in circuit:
        if not circuit[wire].is_input() and circuit[wire].operation == 'AND':
            has_or = False
            for output in circuit[wire].outputs:
                if output.operation == 'OR':
                    has_or = True
                    break
            if not has_or and circuit[wire].input_a.name not in ['x00', 'y00']:
                print(circuit[wire])
                faulty_gates.add(wire)

    print(','.join(sorted(faulty_gates)))
