import re


def read_input(path):
    memory_string = ''

    with open(path, 'r') as file:
        memory_string = file.read()
    return memory_string


def find_mult_instructions(memory_string):
    regex_pattern = r'mul\(([\d]+),([\d]+)\)'

    return re.findall(regex_pattern, memory_string)


def compute_mult_instructions(mult_instructions):
    result = 0

    for instruction in mult_instructions:
        result += int(instruction[0]) * int(instruction[1])
    return result


if __name__ == '__main__':
    test_input_path = './input.in'
    memory_string = read_input(test_input_path)
    # print(memory_string)

    mult_matches = find_mult_instructions(memory_string)
    # print(mult_matches)

    result = compute_mult_instructions(mult_matches)
    print(result)
