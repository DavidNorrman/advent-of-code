
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def read_input(file_path):
    plant_locations = {}

    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            garden_line = list(line.strip())
            for j, plant in enumerate(garden_line):
                if plant not in plant_locations:
                    plant_locations[plant] = set()
                plant_locations[plant].add((i, j))
    return plant_locations


def get_plant_region(locations, current_location,
                     area, fences,
                     visited):

    if current_location not in visited:
        visited.add(current_location)

    adjacent_plants = get_adjacent_plants_and_fences(
        locations, current_location, fences
    )
    area += 1

    if len(adjacent_plants) == 0 or \
            len(adjacent_plants - visited) == 0:
        return area, fences, visited

    for adjacent_plant in adjacent_plants:
        if adjacent_plant not in visited:
            area, fences, visited = \
                get_plant_region(locations,
                                 adjacent_plant,
                                 area, fences,
                                 visited)
    return area, fences, visited


def get_adjacent_plants_and_fences(locations, current_location, fences):
    adjacent_plants = set()
    for direction in directions:
        neighbor = (
            current_location[0] + direction[0],
            current_location[1] + direction[1]
        )
        if neighbor in locations:
            adjacent_plants.add(neighbor)
        else:
            if direction not in fences:
                fences[direction] = []
            fences[direction].append(current_location)
    return adjacent_plants


if __name__ == "__main__":
    plant_locations = read_input('input.in')

    total_cost = 0
    for plant, locations in plant_locations.items():
        # if plant != 'J':
        #     continue
        while len(locations) > 0:
            start_location = next(iter(locations))
            area, fences, visited = get_plant_region(
                locations, start_location, 0, {}, set()
            )
            sides = 0
            for direction in fences:
                dir_sides = 1
                if direction[0] != 0:
                    fences[direction].sort(key=lambda x: (x[0], x[1]))
                    
                    start_side = fences[direction].pop(0)
                    for fence in fences[direction]:
                        if fence[0] != start_side[0] or fence[1] != start_side[1] + 1:
                            dir_sides += 1
                        start_side = fence
                else:
                    fences[direction].sort(key=lambda x: (x[1], x[0]))

                    start_side = fences[direction].pop(0)
                    for fence in fences[direction]:
                        if fence[1] != start_side[1] or fence[0] != start_side[0] + 1:
                            dir_sides += 1
                        start_side = fence
                
                #print(f"Fence: {direction} -> {fences[direction]}, sides: {dir_sides}")
                sides += dir_sides


            # print(f"Plant {plant} -> {area * sides} = {area} * {sides}")
            total_cost += area * sides
            locations = locations - visited

    print(f"Total cost: {total_cost}")
