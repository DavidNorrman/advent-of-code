

directions = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def read_input(input_file_path):
    topographical_map = []
    trailhead_coordinates = []
    with open(input_file_path) as file:
        for i, line in enumerate(file):
            topographical_map.append([])
            for j, height in enumerate(line.strip()):
                topographical_map[i].append(int(height))
                if height == '0':
                    trailhead_coordinates.append((i, j))

    return topographical_map, trailhead_coordinates


def get_trailhead_score(topographical_map, start_coordinate, found_peaks):
    current_height = (
        topographical_map[start_coordinate[0]][start_coordinate[1]]
    )

    # print(start_coordinate, current_height)

    if current_height == 9:
        # print('Found peak at', start_coordinate)
        return found_peaks.append(start_coordinate)

    for direction in directions:
        next_coordinate = (
            start_coordinate[0] + direction[0],
            start_coordinate[1] + direction[1],
        )
        if in_map_bounds(topographical_map, next_coordinate):
            next_height = topographical_map[next_coordinate[0]][next_coordinate[1]]
            if next_height == current_height + 1:
                get_trailhead_score(topographical_map, next_coordinate, found_peaks)
            else:
                continue

    return found_peaks


def in_map_bounds(topographical_map, coordinate):
    return (
        0 <= coordinate[0] < len(topographical_map) and
        0 <= coordinate[1] < len(topographical_map[0])
    )


if __name__ == '__main__':
    topographical_map, trailhead_coordinates = read_input('input.in')

    total_paths = 0
    total_peaks = 0
    for trailhead_coordinate in trailhead_coordinates:
        found_peaks = get_trailhead_score(topographical_map, trailhead_coordinate, [])

        total_peaks += len(set(found_peaks))
        total_paths += len(found_peaks)

    # Part 1:
    print(f'Total peaks: {total_peaks}')
    # Part 2:
    print(f'Total paths: {total_paths}')
