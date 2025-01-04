import re
from sympy import symbols, Eq, solve


def read_input(file_path, error_correction=False):
    claw_machines = []
    with open(file_path, 'r') as file:
        while True:
            button_a_line = file.readline().strip()
            if not button_a_line:
                break
            a_match = re.search(r'X\+(\d+), Y\+(\d+)', button_a_line)
            button_a_values = (int(a_match.group(1)), int(a_match.group(2)))

            button_b_line = file.readline().strip()
            b_match = re.search(r'X\+(\d+), Y\+(\d+)', button_b_line)
            button_b_values = (int(b_match.group(1)), int(b_match.group(2)))

            price_line = file.readline().strip()
            price_match = re.search(r'X\=(\d+), Y\=(\d+)', price_line)
            price_values = (int(price_match.group(1)), int(price_match.group(2)))

            if error_correction:
                error = 10000000000000
                price_values = (price_values[0] + error, price_values[1] + error)

            claw_machines.append({
            'button_a': button_a_values,
            'button_b': button_b_values,
            'price': price_values
            })

            file.readline()
    return claw_machines


if __name__ == '__main__':
    claw_machines = read_input('input.in', error_correction=True)

    total_cost = 0
    for claw_machine in claw_machines:
        # print(f'Button A: {claw_machine["button_a"]}, Button B: {claw_machine["button_b"]}, Price: {claw_machine["price"]}')

        n, m = symbols('n m', integer=True)

        x_equation = Eq(n * claw_machine['button_a'][0] + m * claw_machine['button_b'][0], claw_machine['price'][0])
        y_equation = Eq(n * claw_machine['button_a'][1] + m * claw_machine['button_b'][1], claw_machine['price'][1])
        vars, solutions = solve((x_equation, y_equation), (n, m), set=True)
        
        if len(solutions) == 0:
            # print('No solution')
            continue

        solution = solutions.pop()
        cost = 3 * solution[0] + solution[1]

        # print(f'n: {solution[0]}, m: {solution[1]}')
        # print(f'Cost: {cost}')
        total_cost += cost

    print(total_cost)