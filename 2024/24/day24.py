import networkx as nx
import matplotlib.pyplot as plt

class Gate:
    def __init__(self, name, value=None, logic=None):
        self.name = name
        self.value = value
        self.logic = logic
        if logic is not None:
            self.input_a = logic[0]
            self.input_b = logic[1]
            self.operation = logic[2]

    def get_output(self):
        if self.value is not None:
            return self.value
        if self.operation is not None:
            self.value = apply_operation(
                self.input_a.get_output(), self.operation, self.input_b.get_output()
            )
            return self.value
    
    def __repr__(self):
        if self.operation is not None:
            return f'{self.name}: {self.operation[0].name} {self.operation[2]} {self.operation[1].name} -> {self.value}'
        else: return f'{self.name}: {self.value}'

def AND(wire_1, wire_2): return wire_1 & wire_2
def OR(wire_1, wire_2): return wire_1 | wire_2
def XOR(wire_1, wire_2): return wire_1 ^ wire_2

def apply_operation(wire_1, operation, wire_2):
    return globals()[operation](int(wire_1), int(wire_2))

def traverse_circuit(circuit, wire):
    if circuit[wire].value is not None:
        return circuit[wire].value
    if circuit[wire].logic is not None:
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
            if wire_a not in circuit:
                circuit[wire_a] = Gate(wire_a)
            if wire_b not in circuit:
                circuit[wire_b] = Gate(wire_b)
            circuit[output_wire] = Gate(output_wire, logic=(circuit[wire_a], circuit[wire_b], operation))

    # Part 1
    z_values = [traverse_circuit(circuit, z_wire) for z_wire in sorted([key for key in circuit if key.startswith('z')], reverse=True)]
    print('Z:', int(''.join([str(z) for z in z_values]), 2))

    # Part 2
    G = nx.DiGraph()
    for wire, gate in circuit.items():
        G.add_node(wire, label=gate.name)
        if gate.logic is not None:
            G.add_edge(gate.input_a.name, wire)
            G.add_edge(gate.input_b.name, wire)

    pos = nx.nx_agraph.graphviz_layout(G, prog="dot")

    node_labels = {wire: gate.operation if gate.logic is not None else gate.value for wire, gate in circuit.items()}
    label_pos = {node: (x, y - 7) for node, (x, y) in pos.items()}
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=7, arrowsize=20)
    nx.draw_networkx_labels(G, label_pos, node_labels, font_size=12, font_color="black")
    plt.title("Graph Layout")
    plt.show()

    # Checking if the circuit is correct
    x_values = ''.join([str(circuit[x_wire]) for x_wire in sorted([key for key in circuit if key.startswith('x')], reverse=True)])
    y_values = ''.join([str(circuit[y_wire]) for y_wire in sorted([key for key in circuit if key.startswith('y')], reverse=True)])
    print('X:', int(x_values, 2), '+ Y:', int(y_values, 2), '=', int(x_values, 2) + int(y_values, 2))
    print('Z:', int(z_values, 2))
