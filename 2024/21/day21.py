class Vector:
    def __init__(self, x, y): self.x, self.y = x, y
    def __add__(self, other): return Vector(self.x + other.x, self.y + other.y)
    def __sub__(self, other): return Vector(self.x - other.x, self.y - other.y)

directions = {
    '^': Vector(0, -1), 'v': Vector(0, 1),
    '<': Vector(-1, 0), '>': Vector(1, 0),
}
step_weights = {'<': 0, 'v': 1, '^': 2, '>': 3}

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

def process_keypad_moves(move_dict, keypad):
    for key, loc in keypad.items():
        for next_key, next_loc in keypad.items():
            key_pair = (key, next_key)
            distance = next_loc - loc
            if loc.x == keypad['E'].x and next_loc.y == keypad['E'].y:
                move_dict[key_pair] =  (('>' if distance.x > 0 else '<') * abs(distance.x)) + (('v' if distance.y > 0 else '^') * abs(distance.y))
            elif loc.y == keypad['E'].y and next_loc.x == keypad['E'].x:
                move_dict[key_pair] = (('v' if distance.y > 0 else '^') * abs(distance.y)) +  (('>' if distance.x > 0 else '<') * abs(distance.x))
            else:
                move_dict[key_pair] = ''.join(sorted((
                    (('v' if distance.y > 0 else '^') * abs(distance.y)) +
                    (('>' if distance.x > 0 else '<') * abs(distance.x))
                ), key=lambda step: step_weights[step]))

def run_robots(code, move_dict, remaining_robots, memo):
    if (code, remaining_robots) in memo:  return memo[(code, remaining_robots)]
    if remaining_robots == 0: return len(code)
    code = 'A' + code
    n_steps = sum([run_robots(move_dict[(code[i], code[i+1])] + 'A', move_dict, remaining_robots - 1, memo) for i in range(len(code) - 1)])
    memo[(code[1:], remaining_robots)] = n_steps
    return n_steps

if __name__ == '__main__':
    codes = [line.strip() for line in open('input.in')]
    move_dict = {}
    process_keypad_moves(move_dict, numeric_keypad)
    process_keypad_moves(move_dict, directional_keypad)
    results = [(code, run_robots(code, move_dict, 26, {}) * int(code[:-1])) for code in codes]
    print('Total complexity:', sum(complexity for _, complexity in results))
