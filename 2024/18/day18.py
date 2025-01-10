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


directions = [
    Vector(0, 1), 
    Vector(0, -1),
    Vector(1, 0),
    Vector(-1, 0)
]


def read_input(file):
    coordinates = []
    with open(file) as f:
        for line in f:
            split_line = line.strip().split(',')
            coordinates.append(Vector(int(split_line[0]), int(split_line[1])))
    return coordinates

def get_grid(x_len, y_len):
    grid = []
    for _ in range(x_len):
        grid.append(['.'] * y_len)
    return grid

def simulate_byte_fall(grid, coordinates, nr_of_bytes):
    for i, coordinate in enumerate(coordinates):
        if i == nr_of_bytes:
            break
        grid[coordinate[1]][coordinate[0]] = '#'

def find_path(grid, start, end):
    queue = [(0, start)]
    distances = {start: 0}
    previous_nodes = {start: None}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == end:
            path = []
            while current_node:
                path.append(current_node)
                current_node = previous_nodes[current_node]
            return path[::-1]

        for neighbor in neighbors(grid, current_node):
            distance = current_distance + 1
            if neighbor not in distances or distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))
    return None

def neighbors(grid, location):
    for velocity in directions:
        neighbor = location + velocity
        if in_bounds(grid, neighbor) and grid[neighbor.y][neighbor.x] != '#':
            yield neighbor

def in_bounds(grid, location):
        return 0 <= location.x < len(grid[0]) and 0 <= location.y < len(grid)


if __name__ == '__main__':
    coordinates = read_input('input.in')
    width, height = 71, 71
    
    start = Vector(0, 0)
    end = Vector(width - 1, height - 1)

    grid = get_grid(width, height)
    last_byte = 0
    best_path = find_path(grid, start, end)
    for i, coordinate in enumerate(coordinates):
        grid[coordinate.y][coordinate.x] = '#'

        if coordinate in best_path:
            best_path = find_path(grid, start, end)
            if best_path is None:
                last_byte = i
                break
            
    last_coordinate = f"{coordinates[last_byte].x},{coordinates[last_byte].y}"
    print("Last byte to escape:", last_byte) 
    print("Last coordinate:", last_coordinate)