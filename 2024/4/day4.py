
def read_input(input_file_path):
    word_search_matrix = []
    with open(input_file_path, 'r') as file:
        for line in file:
            word_search_matrix.append(list(line.strip()))
    return word_search_matrix


def find_xmases(word_search_matrix):
    xmas_count = 0

    for i, row in enumerate(word_search_matrix):
        for j, letter in enumerate(row):
            if letter == "X":
                xmases = check_around_x(word_search_matrix, i, j)
                xmas_count += xmases
    return xmas_count


def check_around_x(word_search_matrix, i, j):
    xmases = 0

    directions = [
        (0, -1),  # left
        (0, 1),  # right
        (1, 0),  # down
        (-1, 0),  # up
        (-1, 1),  # up-right
        (-1, -1),  # up-left
        (1, 1),  # down-right
        (1, -1),  # down-left
    ]

    for di, dj in directions:
        if check_direction(word_search_matrix, i, j, di, dj):
            # print(f"Found XMAS at direction ({di}, {dj}) at", i, j)
            xmases += 1
    return xmases


def check_direction(word_search_matrix, i, j, di, dj):
    if 0 <= i + 3 * di < len(word_search_matrix) \
            and 0 <= j + 3 * dj < len(word_search_matrix[0]):
        if word_search_matrix[i + di][j + dj] == "M" \
                and word_search_matrix[i + 2 * di][j + 2 * dj] == "A" \
                and word_search_matrix[i + 3 * di][j + 3 * dj] == "S":
            return True
    return False


if __name__ == '__main__':
    input = read_input('./input.in')

    # for row in input:
    #     print(' '.join(row))

    total_xmases = find_xmases(input)
    print(total_xmases)
