from tqdm import tqdm


def read_input(file_path):
    with open(file_path, 'r') as file:
        return [int(x) for x in file.read().strip().split(' ')]


def update_stone(stones, stone_index):
    stone = stones[stone_index]

    if stone == 0:
        stones[stone_index] = 1
        return stone_index + 1
    elif len(str(stone)) % 2 == 0:
        first_stone_half = int(str(stone)[:len(str(stone))//2])
        second_stone_half = int(str(stone)[len(str(stone))//2:])
        new_stones = [first_stone_half, second_stone_half]
        stones[stone_index:stone_index + 1] = new_stones
        return stone_index + 2
    else:
        stones[stone_index] = stone * 2024
        return stone_index + 1


def blink(stones):
    stone_index = 0
    while stone_index < len(stones):
        stone_index = update_stone(stones, stone_index)


if __name__ == '__main__':
    stones = read_input('input.in')
    print(stones)

    for i in tqdm(range(25)):
        blink(stones)
        # print(len(stones))

    print(f"Number of stones: {len(stones)}")
