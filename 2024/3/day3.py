import re

VERBOSE = False


def read_input(path):
    memory_string = ''

    with open(path, 'r') as file:
        memory_string = file.read()
    return memory_string


def find_mult_instructions(memory_string):
    regex_pattern = r"mul\(([\d]+),([\d]+)\)|(don't\(\))|(do\(\))"

    return re.findall(regex_pattern, memory_string)


def compute_mult_instructions(mult_instructions, include_conditionals=False):
    result = 0

    do_flag = True
    for i, instruction_tuple in enumerate(mult_instructions):
        if VERBOSE:
            print(i, instruction_tuple)

        if include_conditionals and instruction_tuple[2] == "don't()":
            do_flag = False
        elif instruction_tuple[3] == "do()":
            do_flag = True
        elif do_flag:
            result += int(instruction_tuple[0]) * int(instruction_tuple[1])

    return result


if __name__ == '__main__':
    test_input_path = './input.in'
    memory_string = read_input(test_input_path)
    # print(memory_string)

    mult_matches = find_mult_instructions(memory_string)
    result = compute_mult_instructions(mult_matches, include_conditionals=True)
    print(result)
