
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))
    
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __repr__(self):
        return f'({self.x}, {self.y})'


directions = {
    '<': Vector(-1, 0),
    'v': Vector(0, 1),
    '^': Vector(0, -1),
    '>': Vector(1, 0),
}
steps_value = {'<': 5, 'v': 4, '^': 3, '>': 2, 'A': 1}

directional_keypad = {
    'E': Vector(0, 0), '^': Vector(1, 0), 'A': Vector(2, 0),
    '<': Vector(0, 1), 'v': Vector(1, 1), '>': Vector(2, 1),
}

numeric_keypad = {
    '7': Vector(0, 0), '8': Vector(1, 0), '9': Vector(2, 0),
    '4': Vector(0, 1), '5': Vector(1, 1), '6': Vector(2, 1),
    '1': Vector(0, 2), '2': Vector(1, 2), '3': Vector(2, 2),
    'E': Vector(0, 3), '0': Vector(1, 3), 'A': Vector(2, 3),
} 

def get_keypad_directions(code, keypad):
    key_pointer = 'A'
    steps = []
    for char in code:
        current_location = keypad[key_pointer]
        next_location = keypad[char]
        if char != key_pointer:
            new_steps = get_required_steps(current_location, next_location)
            optimized_steps = optimize_steps(current_location, new_steps, keypad)
            steps.extend(optimized_steps)
        steps.append('A')
        key_pointer = char
    return steps

def get_required_steps(location, next_location):
    distance = next_location - location
    steps = []
    steps.extend('>' * distance.x if distance.x > 0 else '<' * abs(distance.x))
    steps.extend('v' * distance.y if distance.y > 0 else '^' * abs(distance.y))
    return steps

def optimize_steps(location, steps, keypad):
    steps.sort(key=lambda step: steps_value[step], reverse=True)
    grouped_steps = group_steps(steps)

    for i in range(len(grouped_steps) - 1):
        step, count = grouped_steps[i]
        for _ in range(count):
            if is_illegal_position(location + directions[step], keypad):
                grouped_steps[i], grouped_steps[i + 1] = grouped_steps[i + 1], grouped_steps[i]
                break
            location += directions[step]

    return [step for step, count in grouped_steps for _ in range(count)]

def is_illegal_position(location, keypad):
    return location == keypad['E']

def group_steps(steps):
    grouped_steps = []
    current_char = steps[0]
    count = 0
    for step in steps:
        if step == current_char:
            count += 1
        else:
            grouped_steps.append((current_char, count))
            current_char = step
            count = 1
    grouped_steps.append((current_char, count))
    return grouped_steps

if __name__ == '__main__':
    codes = [line.strip() for line in open('input.in')]

    total_complexity = 0
    for code in codes:
        num_steps = get_keypad_directions(code, numeric_keypad)
        dir_steps_one = get_keypad_directions(num_steps, directional_keypad)
        dir_steps_two = get_keypad_directions(dir_steps_one, directional_keypad)

        # print(f'{code}:', ''.join(code))
        # print(f'{code}:', ''.join(num_steps))
        # print(f'{code}:', ''.join(dir_steps_one))
        # print(f'{code}:', ''.join(dir_steps_two))

        complexity = len(dir_steps_two) * int(code[:-1])
        print(f'Lenght: {len(dir_steps_two)}, Code nr: {int(code[:-1])}, Complexity:', complexity)
        total_complexity += complexity
    print('Total complexity:', total_complexity)


        
