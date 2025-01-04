import numpy as np
import matplotlib.pyplot as plt


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


def get_safety_factor(robot_positions, dimensions):
    quadrant_indices = [
        (robot_positions[:, 0] < dimensions[0] // 2) & (robot_positions[:, 1] < dimensions[1] // 2),
        (robot_positions[:, 0] > dimensions[0] // 2) & (robot_positions[:, 1] < dimensions[1] // 2),
        (robot_positions[:, 0] < dimensions[0] // 2) & (robot_positions[:, 1] > dimensions[1] // 2),
        (robot_positions[:, 0] > dimensions[0] // 2) & (robot_positions[:, 1] > dimensions[1] // 2)
    ]
    safety_factor = np.sum(quadrant_indices, axis=1).prod()
    return safety_factor


def simulate_robots(robot_positions, robot_velocities, time, dimensions):
    return (robot_positions + robot_velocities * time) % np.array(dimensions)


if __name__ == '__main__':
    robot_positions, robot_velocities = read_input('input.in')
    dimensions = np.array([101, 103])

    # Part 1
    robots_at_100s = simulate_robots(robot_positions, robot_velocities, 100, dimensions)
    safety_factor = get_safety_factor(robots_at_100s, dimensions)
    print(safety_factor)

    # Part 2
    start = 0 # after you notice a pattern, start at the first occurrence of the pattern
    stop = 10000
    step = 1 # set the step size after you notice a pattern
    safety_factors = np.zeros(stop)

    plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    scatter = ax1.scatter(robot_positions[:, 0], robot_positions[:, 1])
    ax1.set_xlim(0, dimensions[0] - 1)
    ax1.set_ylim(0, dimensions[1] - 1)
    ax1.invert_yaxis()

    ax1.axhline(y=dimensions[1] // 2, color='red', linestyle='-')
    ax1.axvline(x=dimensions[0] // 2, color='red', linestyle='-')

    line, = ax2.plot([], [], 'b-')
    ax2.set_xlim(start, stop)
    ax2.set_ylim(0, np.max(safety_factors) + 1)
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Safety Factor')

    lowest_safety_factor = np.inf
    for i in range(start, stop, step):
        new_robot_positions = simulate_robots(robot_positions, robot_velocities, i, dimensions)
        scatter.set_offsets(new_robot_positions)

        safety_factors[i] = get_safety_factor(new_robot_positions, dimensions)
        if safety_factors[i] < lowest_safety_factor:
            lowest_safety_factor = safety_factors[i]
            ax2.set_title(f"Lowest Safety Factor: {lowest_safety_factor} at {i} seconds")

        line.set_data(np.arange(start, i + 1), safety_factors[start:i + 1])
        ax2.set_ylim(0, np.max(safety_factors) + 1)

        ax1.set_title(f"Seconds: {i}")

        plt.draw()
        plt.pause(0.05)

    plt.ioff()
    plt.show()
