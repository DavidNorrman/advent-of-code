import heapq

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError('Index out of range')


direction_dict = {
    '>': Vector(0, 1),
    'v': Vector(1, 0),
    '<': Vector(0, -1),
    '^': Vector(-1, 0),
}


def read_input(file_path):
    maze = []
    with open(file_path, 'r') as f:
        for line in f:
            maze.append(list(line.strip()))
    return maze


def construct_maze_graph(maze):
    graph = {}
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] != '#':
                graph[Vector(i, j)] = possible_moves(maze, Vector(i, j))
    return graph


def get_move_weight(current_dir, move_dir):
    clockwise_order = ['>', 'v', '<', '^']
    counterclockwise_order = ['>', '^', '<', 'v']

    clockwise_cost = (clockwise_order.index(move_dir) - clockwise_order.index(current_dir)) % 4
    counterclockwise_order = (counterclockwise_order.index(move_dir) - counterclockwise_order.index(current_dir)) % 4

    return 1 + min(clockwise_cost, counterclockwise_order) * 1000


def find_symbol(maze, symbol):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == symbol:
                return Vector(i, j)
    return None


def can_move(maze, location, direction):
    new_location = location + direction_dict[direction]

    if maze[new_location[0]][new_location[1]] == '#':
        return False

    return True


def possible_moves(maze, location):
    moves = []
    for d in direction_dict:
        if can_move(maze, location, d):
            new_location = location + direction_dict[d]
            moves.append((new_location, d))
    return moves


def find_path(maze_graph, start, end, start_direction):
    queue = [(0, start, start_direction)]
    costs = {start: 0}
    paths = {start: [(start, start_direction)]}

    while queue:
        current_cost, current_location, current_direction = heapq.heappop(queue)

        if current_location == end:
            print('End found')
            return current_cost, paths[current_location]
        
        for move in maze_graph[current_location]:
            new_location, new_direction = move
            new_cost = current_cost + get_move_weight(current_direction, new_direction)
            
            if new_location not in costs or new_cost < costs[new_location]:
                costs[new_location] = new_cost
                heapq.heappush(queue, (new_cost, new_location, new_direction))
                paths[new_location] = paths[current_location] + [(new_location, new_direction)]
    return -1


if __name__ == '__main__':
    maze = read_input('input.in')
    start = find_symbol(maze, 'S')
    end = find_symbol(maze, 'E')
    start_direction = '>'

    maze_graph = construct_maze_graph(maze)
    cost, path = find_path(maze_graph, start, end, start_direction)

    for location, direction in path:
        if maze[location.x][location.y] not in ['S', 'E']:
            maze[location.x][location.y] = direction

    for line in maze:
        print(''.join(line))

    print(f'Cost: {cost}')
