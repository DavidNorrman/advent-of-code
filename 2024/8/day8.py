

def read_input(input_file_path):
    city_map = []
    antennae = {}
    with open(input_file_path, 'r') as file:
        for i, line in enumerate(file):
            city_map.append([])
            for j, char in enumerate(list(line.strip())):
                city_map[i].append(char)
                if char != '.':
                    if char not in antennae:
                        antennae[char] = []
                    antennae[char].append((i, j))

    return city_map, antennae


def get_antinodes(antennae, city_bounds):
    antinodes = []
    for i, antenna_a in enumerate(antennae):
        for j, antenna_b in enumerate(antennae):
            if i != j:
                antinode_direction = subtract_coordinates(antenna_a, antenna_b)
                antinode = antenna_a
                while in_bounds(antinode, city_bounds):
                    antinodes.append(antinode)
                    antinode = add_coordinates(antinode, antinode_direction)
    return antinodes


def in_bounds(coordinate, bounds):
    return 0 <= coordinate[0] < bounds[0] and 0 <= coordinate[1] < bounds[1]


def subtract_coordinates(coordinate_a, coordinate_b):
    return tuple(a - b for a, b in zip(coordinate_a, coordinate_b))


def add_coordinates(coordinate_a, coordinate_b):
    return tuple(a + b for a, b in zip(coordinate_a, coordinate_b))


if __name__ == '__main__':
    city_map, antennae = read_input('input.in')

    # for line in city_map:
    #     print(''.join(line))

    total_antinodes = []
    for key in antennae:
        antinodes = get_antinodes(
            antennae[key],
            (len(city_map), len(city_map[0]))
        )
        # print(f'{key} - {antennae[key]}')
        # print(antinodes)
        total_antinodes.extend(antinodes)

    print(f'total antinodes: {len(set(total_antinodes))}')
