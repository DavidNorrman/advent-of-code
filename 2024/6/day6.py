import time
from copy import deepcopy
from tqdm import tqdm

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

    if lab_grid[new_location[0]][new_location[1]] != '#' \
            and lab_grid[new_location[0]][new_location[1]] != 'O':
        lab_grid[guard_location[0]][guard_location[1]] = 'X'
        guard_location = new_location
        accessed_cells.append((new_location, guard))

        lab_grid[guard_location[0]][new_location[1]] = guard
        return lab_grid, guard_location, accessed_cells
    else:
        # print('Turning')
        lab_grid[guard_location[0]][guard_location[1]] = guard_rotation[guard]

    return lab_grid, guard_location, accessed_cells


def guard_out_of_bounds(lab_grid, guard_location):
    return guard_location[0] < 0 or guard_location[0] >= len(lab_grid) or \
           guard_location[1] < 0 or guard_location[1] >= len(lab_grid[0])


def is_looping(accessed_cells):
    return len(accessed_cells) != len(set(accessed_cells))


def get_guard(lab_grid, guard_location):
    return lab_grid[guard_location[0]][guard_location[1]]


def print_lab_grid(lab_grid):
    for row in lab_grid:
        print(row)


def clear_previous_output(rows):
    print("\033[F" * rows, end="")


def animate_lab_grid(lab_grid, print_loops=False, loops=0):
    print_lab_grid(lab_grid)
    if print_loops:
        print("\n")
        print(f"Loops: {loops}")
    time.sleep(0.025)
    clear_previous_output(len(lab_grid) + 3)


if __name__ == '__main__':
    lab_grid, guard_location = read_input('./input.in')
    lab_start = deepcopy(lab_grid)
    guard_start_location = guard_location

    accessed_cells = []
    guard = get_guard(lab_grid, guard_location)
    accessed_cells.append((guard_start_location, guard))

    while (guard_location != (-1, -1)):
        lab_grid, guard_location, accessed_cells = get_next_move(
            lab_grid, guard_location, accessed_cells
        )
        # animate_lab_grid(lab_grid)

    accessed_coordinates = set([cell[0] for cell in accessed_cells])
    print(f"Accessed cells: {len(set(accessed_coordinates))}")

    blockable_cells = accessed_coordinates
    blockable_cells.discard(guard_start_location)

    loops = 0
    for blockage in tqdm(blockable_cells):
        blocked_lab_grid = deepcopy(lab_start)
        blocked_lab_grid[blockage[0]][blockage[1]] = 'O'
        accessed_cells = []
        accessed_cells.append((guard_start_location, guard))

        guard_location = guard_start_location

        while (guard_location != (-1, -1)):
            if is_looping(accessed_cells):
                loops += 1
                break

            blocked_lab_grid, guard_location, accessed_cells = get_next_move(
                blocked_lab_grid, guard_location, accessed_cells
            )
            # animate_lab_grid(blocked_lab_grid, print_loops=True, loops=loops)
    print(f"Loops: {loops}")
