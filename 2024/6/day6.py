
guard_velocity = {
    '^': (-1, 0),
    '>': (0, 1),
    'v': (1, 0),
    '<': (0, -1),
}

guard_rotation = {
    '^': '>',
    '>': 'v',
    'v': '<',
    '<': '^'
}


def read_input(input_file_path):
    guard_chars = ['^', 'v', '<', '>']
    guard_location = (0, 0)

    lab_grid = []
    with open(input_file_path, 'r') as file:
        for line in file:
            lab_grid.append(list(line.strip()))
            for guard in guard_chars:
                if guard in lab_grid[-1]:
                    guard_location = (len(lab_grid) - 1,
                                      lab_grid[-1].index(guard))

    return lab_grid, guard_location


def get_next_move(lab_grid, guard_location, accessed_cells):
    guard = lab_grid[guard_location[0]][guard_location[1]]
    velocity = guard_velocity[guard]

    new_location = (guard_location[0] + velocity[0],
                    guard_location[1] + velocity[1])

    if guard_out_of_bounds(lab_grid, new_location):
        return lab_grid, (-1, -1), accessed_cells

    if lab_grid[new_location[0]][new_location[1]] != '#':
        lab_grid[guard_location[0]][guard_location[1]] = 'X'
        guard_location = new_location
        accessed_cells.append(new_location)

        lab_grid[guard_location[0]][new_location[1]] = guard
        return lab_grid, guard_location, accessed_cells
    else:
        # print('Turning')
        lab_grid[guard_location[0]][guard_location[1]] = guard_rotation[guard]

    return lab_grid, guard_location, accessed_cells


def guard_out_of_bounds(lab_grid, guard_location):
    return guard_location[0] < 0 or guard_location[0] >= len(lab_grid) or \
           guard_location[1] < 0 or guard_location[1] >= len(lab_grid[0])


if __name__ == '__main__':
    lab_grid, guard_location = read_input('./input.in')
    accessed_cells = []
    accessed_cells.append(guard_location)

    while (guard_location != (-1, -1)):
        lab_grid, guard_location, accessed_cells = get_next_move(
            lab_grid, guard_location, accessed_cells
        )
        # for row in lab_grid:
        #     print(row)
        # print('\n')

    print(len(set(accessed_cells)))
