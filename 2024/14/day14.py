import numpy as np


def read_input(file_path):
    robot_positions = []
    robot_velocities = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            position = tuple(map(int, parts[0][2:].split(',')))
            robot_positions.append(position)
            velocity = tuple(map(int, parts[1][2:].split(',')))
            robot_velocities.append(velocity)
    
    robot_positions = np.array(robot_positions)
    robot_velocities = np.array(robot_velocities)
    return robot_positions, robot_velocities


if __name__ == '__main__':
    robot_positions, robot_velocties = read_input('input.in')
    width = 101
    height = 103

    new_robot_positions = (robot_positions + robot_velocties * 100) % (width, height)

    quadrant_indices = [
        (new_robot_positions[:, 0] <= width // 2 - 1) & (new_robot_positions[:, 1] <= height // 2 - 1),
        (new_robot_positions[:, 0] >= width // 2 + 1) & (new_robot_positions[:, 1] <= height // 2 - 1),
        (new_robot_positions[:, 0] <= width // 2 - 1) & (new_robot_positions[:, 1] >= height // 2 + 1),
        (new_robot_positions[:, 0] >= width // 2 + 1) & (new_robot_positions[:, 1] >= height // 2 + 1)
    ]
    safety_factor = np.sum(quadrant_indices, axis=1).prod()
    
    print(safety_factor)