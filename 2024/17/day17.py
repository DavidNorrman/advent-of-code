class ThreeBitComputer:
    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C
        self.instruction_pointer = 0

        self.instructions = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

    def perform_instruction(self, instruction, operand):
        return self.instructions[instruction](operand)

    def combo_operand(self, index):
        if 0 <= index <= 3:
            return index
        elif index == 4:
            return self.A
        elif index == 5:    
            return self.B
        elif index == 6:
            return self.C
        return None

    def dv(self, x):
        self.instruction_pointer += 2
        return self.A // (2 ** self.combo_operand(x))

    def adv(self, x):
        self.A = self.dv(x)

    def bdv(self, x):
        self.B = self.dv(x)

    def cdv(self, x):
        self.C = self.dv(x)

    def bxl(self, x):
        self.B = self.B ^ x
        self.instruction_pointer += 2

    def bst(self, x):
        self.B = self.combo_operand(x) % 8
        self.instruction_pointer += 2

    def jnz(self, x):
        if self.A != 0:
            self.instruction_pointer = x
        else:
            self.instruction_pointer += 2

    def bxc(self, x):
        self.B = self.B ^ self.C
        self.instruction_pointer += 2

    def out(self, x):
        self.instruction_pointer += 2
        return self.combo_operand(x) % 8


def read_input(file):
    program_code = []
    with open(file, 'r') as f:
        register_a_line = f.readline().strip()
        register_b_line = f.readline().strip()
        register_c_line = f.readline().strip()

        A = int(register_a_line.split(' ')[2])
        B = int(register_b_line.split(' ')[2])
        C = int(register_c_line.split(' ')[2])

        f.readline()
        program_code = [int(i) for i in f.readline().strip().split(' ')[1].split(',')]
    return A, B, C, program_code


def compiled_program(a, b):
    # "compiled" program code, returns the result from the out step
    return (((b ^ 2) ^ ((a + b) >> (b ^ 2))) ^ 7) & 7


if __name__ == '__main__':
    A,B,C, program_code = read_input('input.in')
    
    # Part 1
    print("Part 1")
    # set A to verify part 2: A = ...
    tbc = ThreeBitComputer(A, B, C)

    outputs = []
    while tbc.instruction_pointer < len(program_code):
        instruction = int(program_code[tbc.instruction_pointer])
        operand = int(program_code[tbc.instruction_pointer + 1])
        out_value = tbc.perform_instruction(instruction, operand)

        if out_value is not None:
            outputs.append(out_value)

    output_string = ','.join(map(str, outputs))
    print(output_string, '\n')

    # Part 2
    print("Part 2")
    a = 0
    for i, nr in enumerate(program_code[::-1]):
        a = a << 3
        for b in range(8):
            out = compiled_program(a, b)
            if out == nr:
                a += b
                break
    print(a)



