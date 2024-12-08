
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


def find_x_mases(word_search_matrix):
    x_mas_count = 0
    for i, row in enumerate(word_search_matrix):
        for j, letter in enumerate(row):
            if letter == "A" and x_fits(word_search_matrix, i, j):
                x_mases = check_around_a(word_search_matrix, i, j)
                x_mas_count += x_mases
    return x_mas_count


def x_fits(word_search_matrix, i, j):
    return 0 <= i - 1 \
        and 0 <= j - 1 \
        and 0 <= i + 1 < len(word_search_matrix) \
        and 0 <= j + 1 < len(word_search_matrix[0])


def check_around_a(word_search_matrix, i, j):
    x_mases = 0

    # up-left to down-right
    if (word_search_matrix[i - 1][j - 1] == "M"
            and word_search_matrix[i + 1][j + 1] == "S") \
            or (word_search_matrix[i - 1][j - 1] == "S"
                and word_search_matrix[i + 1][j + 1] == "M"):
        # up-right to down-left
        if (word_search_matrix[i - 1][j + 1] == "M"
                and word_search_matrix[i + 1][j - 1] == "S") \
                or (word_search_matrix[i - 1][j + 1] == "S"
                    and word_search_matrix[i + 1][j - 1] == "M"):
            x_mases += 1
            # print(f"Found XMAS at ({i}, {j})")

    return x_mases


if __name__ == '__main__':
    input = read_input('./input.in')

    # for row in input:
    #     print(' '.join(row))

    # total_xmases = find_xmases(input)
    # print(total_xmases)

    total_x_mases = find_x_mases(input)
    print(total_x_mases)
