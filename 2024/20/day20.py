directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def read_input(file):
    with open(file) as f:
        return [list(line.strip()) for line in f]

def find_symbol(maze, symbol):
    for i, line in enumerate(maze):
        for j, cell in enumerate(line):
            if cell == symbol:
                return (i, j)
            
def get_race_path(maze, start, end):
    current = start
    time = 0
    path = {start: time}
    while current != end:
        for direction in directions:
            new = move(current, direction)
            if new not in path and maze[new[0]][new[1]] != '#':
                time += 1
                path[new] = time
                current = new
                break
    return path

def get_possible_cheats(path, location):
    for direction in directions:
        wall_location = move(location, direction)
        cheat_location = move(wall_location, direction)
        if (wall_location not in path 
                and cheat_location in path 
                and path[cheat_location] > path[location]):
            yield cheat_location

def move(location, direction):
    return (location[0] + direction[0], location[1] + direction[1])

def get_time_saved(path, location, cheat_location, distance=2):
    return (path[cheat_location] - path[location]) - distance

if __name__ == '__main__':
    maze = read_input('input.in')
    start = find_symbol(maze, 'S')
    end = find_symbol(maze, 'E')

    path = get_race_path(maze, start, end)
    at_least_100 = 0

    # Part 1
    # for location in path:
    #     for cheat_location in get_possible_cheats(path, location):
    #         time_saved = get_time_saved(path, location, cheat_location)
    #         if time_saved >= 100:
    
    # Part 2
    max_distance = 20
    for location in path:
        for i in range(-max_distance, max_distance + 1):
            for j in range(-max_distance + abs(i), max_distance + 1 - abs(i)):
                cheat_location = move(location, (i, j))
                if cheat_location in path and path[cheat_location] > path[location]:
                    time_saved = get_time_saved(path, location, cheat_location, abs(i) + abs(j))
                    if time_saved >= 100:
                        at_least_100 += 1
    
    print("Nr cheats with time saved >= 100:", at_least_100)