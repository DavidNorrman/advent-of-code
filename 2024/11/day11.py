from functools import lru_cache


def read_input(file_path):
    with open(file_path, 'r') as file:
        return [int(x) for x in file.read().strip().split(' ')]


@lru_cache(maxsize=None)
def evolve_stone(blinks, stone):
    if blinks == 0:
        return 1

    if stone == 0:
        result = evolve_stone(blinks - 1, 1)
    else:
        stone_str = str(stone)
        if len(stone_str) % 2 == 0:
            mid = len(stone_str) // 2
            first_stone_half = int(stone_str[:mid])
            second_stone_half = int(stone_str[mid:])
            result = (evolve_stone(blinks - 1, first_stone_half) +
                      evolve_stone(blinks - 1, second_stone_half))
        else:
            result = evolve_stone(blinks - 1, stone * 2024)
    return result


def process_stones(stones, blinks):
    total_stones = 0
    for stone in stones:
        total_stones += evolve_stone(blinks, stone)
        # print("Done with stone")

    return total_stones


if __name__ == '__main__':
    stones = read_input('input.in')
    # print(stones)

    blinks = 75
    evolved_stone_count = process_stones(stones, blinks)

    print(f"Number of stones: {evolved_stone_count}")
    # print(f"Evolutions: {evolved_stones}")
