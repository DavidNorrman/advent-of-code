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
    with open(file_path, 'r') as file:
        reading_warehouse = True
        for line in file:
            if line == '\n':
                reading_warehouse = False
                continue
            if reading_warehouse:
                warehouse.append(list(line.strip()))
            else:
                robot_path.extend(line.strip())
    return warehouse, robot_path


def find_robot(warehouse):
    for i, row in enumerate(warehouse):
        for j, cell in enumerate(row):
            if cell == '@':
                return (i, j)
    return None


def resize_warehouse(warehouse):
    resize_map = {
        'O': ['[',']'],
        '@': ['@','.'],
        '.': ['.','.'],
        '#': ['#','#'],
    }
    new_warehouse = []
    for row in warehouse:
        new_row = []
        for cell in row:
            new_row.extend(resize_map[cell])
        new_warehouse.append(new_row)
    return new_warehouse


def move(warehouse, position, movement):
    direction = directions[movement]
    next_position = get_new_position(position, direction)
    next_cell = get_cell(warehouse, next_position)

    if next_cell == '#':
        return position
    
    if next_cell == '.':
        set_cell(warehouse, next_position, '@')
        set_cell(warehouse, position, '.')
        return next_position
    elif next_cell in '[]':
        if movement in '<>':
            steps = 0
            while get_cell(warehouse, get_new_position(next_position, direction, steps + 1)) in '[]':
                steps += 1

            if get_cell(warehouse, get_new_position(next_position, direction, steps + 1)) == '#':
                return position

            if get_cell(warehouse, get_new_position(next_position, direction, steps + 1)) == '.':
                for step in range(steps, -1, -1):
                    box_position = get_new_position(next_position, direction, step)
                    new_box_position = get_new_position(box_position, direction)
                    set_cell(warehouse, new_box_position, get_cell(warehouse, box_position))
                    set_cell(warehouse, box_position, '.')

                set_cell(warehouse, next_position, '@')
                set_cell(warehouse, position, '.')
                return next_position
        elif movement in '^v':
            offset = {
                '[': (0, 1),
                ']': (0, -1)
            }

            boxes = []
            boxes.append([next_position, get_new_position(next_position, offset[next_cell])])

            blocked = False
            current_box_layer = 0
            while not blocked:
                if current_box_layer >= len(boxes):
                    break
                current_boxes = boxes[current_box_layer]
                
                new_box_layer = set()
                for box_position in current_boxes:
                    next_box_position = get_new_position(box_position, direction)
                    next_cell = get_cell(warehouse, next_box_position)
                    
                    if next_cell == '#':
                        blocked = True
                        break

                    if next_cell in '[]':
                        new_box_layer.add(next_box_position)
                        new_box_layer.add(get_new_position(next_box_position, offset[next_cell]))

                if len(new_box_layer) > 0:
                    boxes.append(list(new_box_layer))
                current_box_layer += 1

            if blocked:
                return position
            
            for layer in reversed(boxes):
                for box_position in layer:
                    new_box_position = get_new_position(box_position, direction)
                    set_cell(warehouse, new_box_position, get_cell(warehouse, box_position))
                    set_cell(warehouse, box_position, '.')
            
            set_cell(warehouse, next_position, '@')
            set_cell(warehouse, position, '.')
            return next_position
            

def get_cell(warehouse, position):
    return warehouse[position[0]][position[1]]


def set_cell(warehouse, position, value):
    warehouse[position[0]][position[1]] = value


def get_new_position(position, direction, steps=1):
    return position[0] + steps * direction[0], position[1] + steps * direction[1]


def get_gps_distances(warehouse):
    total_distance = 0
    for i, row in enumerate(warehouse):
        for j, cell in enumerate(row):
            if cell == '[':
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


def draw_warehouse(canvas, root, warehouse, direction):
    color_map = {
        '#': "black",
        '@': "blue",
        'O': "red",
        '[': "red",
        ']': "red",
        '.': "white"
    }

    canvas.delete("all")
    for i, row in enumerate(warehouse):
        for j, cell in enumerate(row):
            color = color_map[cell]

            if cell == '@':
                canvas.create_text(
                    j * cell_size + cell_size / 2,
                    i * cell_size + cell_size / 2,
                    text=direction,
                    fill=color,
                    font=("bold", cell_size)
                )
            elif cell == '[':
                canvas.create_text(
                    j * cell_size + cell_size / 2,
                    i * cell_size + cell_size / 2,
                    text='[',
                    fill=color,
                    font="bold"
                )
            elif cell == ']':
                canvas.create_text(
                    j * cell_size + cell_size / 2,
                    i * cell_size + cell_size / 2,
                    text=']',
                    fill=color,
                    font="bold"
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
    warehouse, robot_path = read_input('input.in')
    warehouse = resize_warehouse(warehouse)
    robot_location = find_robot(warehouse)

    root, canvas = set_up_window(warehouse)
    draw_warehouse(canvas, root, warehouse, robot_path[0])
    for movement in robot_path:
        robot_location = move(warehouse, robot_location, movement)
        draw_warehouse(canvas, root, warehouse, movement)
        time.sleep(0.0001)

    gps_distance = get_gps_distances(warehouse)
    print(f"GPS distance: {gps_distance}")
    root.mainloop()
