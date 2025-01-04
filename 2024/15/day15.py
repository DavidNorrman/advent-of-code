import tkinter as tk
import time


directions = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1)
}

cell_size = 20


def read_input(file_path):
    warehouse = []
    robot_path = []
    robot_position = None
    with open(file_path, 'r') as file:
        reading_warehouse = True
        for i, line in enumerate(file):
            if line == '\n':
                reading_warehouse = False
                continue

            if reading_warehouse:
                warehouse.append([])
                for j, char in enumerate(line.strip()):
                    if char == '@':
                        robot_position = (i, j)
                    warehouse[i].append(char)
            else:
                robot_path.extend(line.strip())
    return warehouse, robot_path, robot_position


def move(warehouse, position, direction):
    next_position = (position[0] + direction[0], position[1] + direction[1])
    if warehouse[next_position[0]][next_position[1]] == '#':
        return position
    
    if warehouse[next_position[0]][next_position[1]] == '.':
        warehouse[position[0]][position[1]] = '.'
        warehouse[next_position[0]][next_position[1]] = '@'
        return next_position

    steps = 1
    while warehouse[position[0] + steps * direction[0]][position[1] + steps * direction[1]] == 'O':
        if warehouse[position[0] + (steps + 1) * direction[0]][position[1] + (steps + 1) * direction[1]] == '#':
            return position
        
        if warehouse[position[0] + (steps + 1) * direction[0]][position[1] + (steps + 1) * direction[1]] == '.':
            for i in range(steps + 1, 1, -1):
                warehouse[position[0] + i * direction[0]][position[1] + i * direction[1]] = 'O'
            warehouse[position[0]][position[1]] = '.'
            warehouse[next_position[0]][next_position[1]] = '@'
            return next_position
        steps += 1


def get_gps_distances(warehouse):
    total_distance = 0
    for i, row in enumerate(warehouse):
        for j, cell in enumerate(row):
            if cell == 'O':
                total_distance += 100 * i + j
    return total_distance


def set_up_window(warehouse):
    root = tk.Tk()
    root.title("Warehouse")

    canvas_width = len(warehouse[0]) * cell_size
    canvas_height = len(warehouse) * cell_size
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
    canvas.pack()
    return root, canvas


def draw_warehouse(canvas, root, warehouse, direction=None):
    canvas.delete("all")
    for i, row in enumerate(warehouse):
        for j, cell in enumerate(row):
            color = "white"
            text = None
            if cell == '#':
                color = "black"
            elif cell == '@':
                color = "blue"
                text = direction
            elif cell == 'O':
                color = "red"

            if cell == '@' and direction:
                canvas.create_text(
                    j * cell_size + cell_size / 2,
                    i * cell_size + cell_size / 2,
                    text=text,
                    fill=color,
                    font=("Purisa", cell_size)
                )
            else:
                canvas.create_rectangle(
                    j * cell_size,
                    i * cell_size,
                    j * cell_size + cell_size,
                    i * cell_size + cell_size,
                    fill=color
                )
    root.update()


if __name__ == '__main__':
    warehouse, robot_path, robot_location = read_input('input.in')
    
    root, canvas = set_up_window(warehouse)
    draw_warehouse(canvas, root, warehouse)
    for movement in robot_path:
        robot_location = move(warehouse, robot_location, directions[movement])
        draw_warehouse(canvas, root, warehouse, movement)
        time.sleep(0.01)

    gps_distance = get_gps_distances(warehouse)
    print(f"GPS distance: {gps_distance}")
    root.mainloop()
