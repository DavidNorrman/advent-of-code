import json


def ingest_input(input_path):
    list1 = []
    list2 = []

    with open(input_path, 'r') as file:
        for line in file:
            numbers = line.split()
            list1.append(int(numbers[0]))
            list2.append(int(numbers[1]))

    return list1, list2


def get_list_distance(list1, list2):
    total_distance = 0

    for i in range(len(list1)):
        total_distance += abs(list1[i] - list2[i])
    return total_distance


def get_similarity_score(list1, list2):
    similarity_score = 0

    left_pointer = 0
    right_pointer = 0

    similarity_dict = {}

    # test_counter = 0

    while left_pointer < len(list1) and right_pointer < len(list2):
        # if test_counter > 20:
        #     break

        if list1[left_pointer] not in similarity_dict:
            similarity_dict[list1[left_pointer]] = \
                type('obj', (object,), {'left': 0, 'right': 0})()

        # print(f'left nr: {list1[left_pointer]}')
        # print(f'right nr: {list2[right_pointer]}')

        if list1[left_pointer] == list2[right_pointer]:
            similarity_dict[list1[left_pointer]].right += 1
            right_pointer += 1
            # print('match')
        elif list1[left_pointer] > list2[right_pointer]:
            right_pointer += 1
        else:
            similarity_dict[list1[left_pointer]].left += 1
            left_pointer += 1
            # print('no match')

        # test_counter += 1

    # print(json.dumps({k: v.__dict__ for k, v in similarity_dict.items()}, indent=4))

    for key in similarity_dict:
        similarity_score += \
            key \
            * similarity_dict[key].right \
            * similarity_dict[key].left
    return similarity_score


if __name__ == '__main__':
    test_input_path = './test_input.in'

    input = ingest_input(test_input_path)
    input[0].sort()
    input[1].sort()

    # Part 1
    distance = get_list_distance(input[0], input[1])
    print(distance)

    # Part 2
    similarity_score = get_similarity_score(input[0], input[1])
    print(similarity_score)
