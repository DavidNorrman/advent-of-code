
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
    plant_locations = read_input('test_input.in')

    total_cost = 0
    for plant, locations in plant_locations.items():
        if plant != 'R':
            continue
        while len(locations) > 0:
            start_location = next(iter(locations))
            area, fences, visited = get_plant_region(
                locations, start_location, 0, {}, set()
            )
            for direction in fences:
                print(f"Fence: {direction} -> {fences[direction]}")

            for direction in fences:
                if direction[0] != 0:
                    pass
                else:
                    pass

            print(f"Plant {plant} -> {area} = {area}")
            # total_cost += area * perimiter
            locations = locations - visited

    print(f"Total cost: {total_cost}")
