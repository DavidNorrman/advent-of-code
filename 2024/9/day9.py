
def read_input(input_file_path):
    with open(input_file_path, 'r') as file:
        return file.read()


def expand_disk_map(disk_map):
    expanded_memory_map = []
    free_space_indices = []
    file_location_map = {}
    next_is_file = True
    file_id = 0
    for digit in disk_map:
        if next_is_file:
            file_location_map[file_id] = (
                [x for x in range(len(expanded_memory_map),
                                  len(expanded_memory_map) + int(digit))]
            )
            expanded_memory_map.extend([file_id for _ in range(int(digit))])
            file_id += 1
        else:
            free_space_indices.extend(
                [x for x in range(len(expanded_memory_map),
                                  len(expanded_memory_map) + int(digit))]
            )
            expanded_memory_map.extend(['.' for _ in range(int(digit))])
        next_is_file = not next_is_file
    return (expanded_memory_map,
            free_space_indices,
            file_location_map,
            file_id - 1)


def clean_memory_map(memory_map, free_memory_indices):
    for i in range(len(memory_map) - 1, -1, -1):
        if len(free_memory_indices) == 0 \
                or i < free_memory_indices[0]:
            break

        if memory_map[i] != '.':
            memory_map[free_memory_indices.pop(0)] = memory_map[i]
            memory_map[i] = '.'
            free_memory_indices.append(i)


def reorder_files(memory_map,
                  free_memory_indices,
                  file_location_map,
                  highest_file_id):
    for file_id in range(highest_file_id, -1, -1):
        file_indices = file_location_map[file_id]
        suitable_memory = find_free_memory(free_memory_indices,
                                           len(file_indices))
        if len(suitable_memory) != 0 \
                and suitable_memory[0] < file_indices[0]:
            for i, file_index in enumerate(file_indices):
                memory_map[suitable_memory[i]] = file_id
                memory_map[file_index] = '.'

            for index in suitable_memory:
                free_memory_indices.remove(index)
        # print(f'File {file_id}: {file_indices}')
        # print(f'Free_memory_indices: {free_memory_indices}')
        # print(f'Free space: {suitable_memory}')


def find_free_memory(free_memory_indices, size):
    free_space_index = free_space_indices[0]
    current_indices = [free_space_index]

    if size == 1:
        return current_indices

    for memory_index in free_memory_indices[1:]:
        if memory_index == free_space_index + 1:
            current_indices.append(memory_index)
            free_space_index = memory_index
            if len(current_indices) == size:
                return current_indices
        else:
            free_space_index = memory_index
            current_indices = [free_space_index]
    return []


def calculate_checksum(memory_map):
    checksum = 0
    for i, id in enumerate(memory_map):
        if id != '.':
            checksum += i * id
    return checksum


if __name__ == '__main__':
    disk_map = read_input('input.in')

    expanded_memory_map, free_space_indices, highest_file_id, file_location_map = \
        expand_disk_map(disk_map)

    # Part 1
    # clean_memory_map(expanded_memory_map, free_space_indices)
    # print(''.join([str(x) for x in expanded_memory_map]))

    # Part 2
    reorder_files(
        expanded_memory_map,
        free_space_indices,
        highest_file_id,
        file_location_map
    )
    # print(''.join([str(x) for x in expanded_memory_map]))

    print(f'Checksum: {calculate_checksum(expanded_memory_map)}')
