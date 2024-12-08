

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
    list1.sort()
    list2.sort()
    total_distance = 0

    for i in range(len(list1)):
        total_distance += abs(list1[i] - list2[i])
    return total_distance


if __name__ == '__main__':
    test_input_path = './test_input.in'

    input = ingest_input(test_input_path)
    distance = get_list_distance(input[0], input[1])

    print(distance)
