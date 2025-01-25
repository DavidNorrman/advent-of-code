class Gate:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
        self.outputs = []

    def set_logic(self, input_a, input_b, operation):
        self.input_a = input_a
        self.input_b = input_b
        self.operation = operation
        
    def is_z(self):
        return self.name[0] == 'z'
    
    def is_input(self):
        return self.name[0] in ['x', 'y']
    
    def has_operation(self):
        return hasattr(self, 'operation')
    
    def __repr__(self):
        logic_string = ''
        if not self.is_input():
            input_a = f"{self.input_a.name} - {self.input_a.value}" if self.input_a.is_input() else f"{self.input_a.name} - {self.input_a.operation}"
            input_b = f"{self.input_b.name} - {self.input_b.value}" if self.input_b.is_input() else f"{self.input_b.name} - {self.input_b.operation}"
            logic_string =  f': ({input_a}) {self.operation} ({input_b}) '
        output_string = '' if self.is_z() else '-> (' + ', '.join([(output.name + ' ' + output.operation) for output in self.outputs]) + ')'
        return self.name + ' ' + str(self.value) + logic_string + output_string

def apply_operation(wire_1, operation, wire_2):
    return OPERATIONS[operation](int(wire_1), int(wire_2))

OPERATIONS = {
    'AND': lambda a, b: a & b,
    'OR': lambda a, b: a | b,
    'XOR': lambda a, b: a ^ b
}

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
    with open('input.in') as f:
        for line in f:
            if line == '\n':
                break
            wire, value = line.strip().split(': ')
            circuit[wire] = Gate(wire, value=value)

        for line in f:
            wire_a, operation, wire_b, _, output_wire = line.strip().split(' ')
            for wire in [wire_a, wire_b, output_wire]: 
                if wire not in circuit: 
                  circuit[wire] = Gate(wire)

            circuit[output_wire].set_logic(circuit[wire_a], circuit[wire_b], operation)
            circuit[wire_a].outputs.append(circuit[output_wire])
            circuit[wire_b].outputs.append(circuit[output_wire])

    # Part 1
    z_values = ''.join([str(traverse_circuit(circuit, z_wire)) for z_wire in sorted([key for key in circuit if key.startswith('z')], reverse=True)])
    print('Z:', int(z_values, 2))

    # Part 2
    faulty_gates = set()
    for wire in circuit:
        # Rule 1: if it is a z gate, the operation must be XOR, unless it's the MSB (z45)
        if circuit[wire].is_z() and circuit[wire].operation != 'XOR' and wire != 'z45':
                # print('Rule 1:', circuit[wire])
                faulty_gates.add(wire)

        # Rule 2: if it is not a z gate, and inputs are not x and y, it can't be an XOR gate
        if circuit[wire].has_operation() and not circuit[wire].is_z() \
            and not circuit[wire].input_a.is_input() and not circuit[wire].input_b.is_input() \
            and circuit[wire].operation == 'XOR':
                # print('Rule 2:', circuit[wire])
                faulty_gates.add(wire)

        # Rule 3: if the operation is XOR, and the inputs are x and y, there must be an XOR gate after it, unless it's the LSB (z00)
        if circuit[wire].has_operation() and circuit[wire].operation == 'XOR' \
            and circuit[wire].input_a.is_input() and circuit[wire].input_b.is_input():
                has_xor = any([output.operation == 'XOR' for output in circuit[wire].outputs])
                if not has_xor and wire != 'z00':
                    # print('Rule 3:', circuit[wire])
                    faulty_gates.add(wire)

        # Rule 4: if it is an AND gate, there must be an OR gate after it, unless inputs are x00 / y00
        if not circuit[wire].is_input() and circuit[wire].operation == 'AND':
            has_or = any([output.operation == 'OR' for output in circuit[wire].outputs])
            if not has_or and circuit[wire].input_a.name not in ['x00', 'y00']:
                #print('Rule 4:', circuit[wire])
                faulty_gates.add(wire)

    print(','.join(sorted(faulty_gates)))
