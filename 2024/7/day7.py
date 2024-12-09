import json

operators = ['+', '*', '||']


def read_input(input_file_path):
    equations = {}
    with open(input_file_path, 'r') as file:
        for line in file:
            equation = line.strip().split(':')
            equations[int(equation[0])] = [
                int(x) for x in equation[1].strip().split(' ')
            ]
    return equations


def verify_equation(answer, equation, operators, partial_result=0):
    if len(equation) == 0:
        # print(f'Answer: {answer} - Partial Result: {partial_result}')
        return answer == partial_result

    results = []
    for operator in operators:
        results.append(verify_equation(
            answer, equation[1:], operators,
            custom_eval(partial_result, operator, equation[0])
        ))

    return any(results)


def custom_eval(number_a, operator, number_b):
    if operator == '||':
        return int(str(number_a) + str(number_b))
    elif operator == '+':
        return number_a + number_b
    elif operator == '*':
        return number_a * number_b
    else:
        raise ValueError(f'Invalid operator: {operator}')


if __name__ == '__main__':
    equations = read_input('input.in')
    # print(json.dumps(equations, indent=4))

    test_sum = 0
    for key, value in equations.items():
        correct = verify_equation(
            key, value[1:], operators, partial_result=value[0]
        )
        if correct:
            test_sum += key
        # print(f'{key}: {value} is {"valid" if correct else "invalid"}')

    print(f'Test sum: {test_sum}')
