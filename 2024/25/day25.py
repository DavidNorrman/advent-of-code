from itertools import product

if __name__ == '__main__':
    keys = []
    locks = []
    line_length = 7
    with open('input.in') as f:
        item_array = []
        for line in f:
            if line == '\n':
                continue

            item_array.append(list(line.strip()))
            if len(item_array) == line_length:
                column_counts = [sum(1 for row in item_array if row[i] == '#') - 1 for i in range(len(item_array[0]))]
                if item_array[0] == ['#'] * 5:
                    locks.append(column_counts)
                else:
                    keys.append(column_counts)
                item_array = []

    nr_keys_that_fit = 0
    for key, lock in product(keys, locks):
        pin_sum = [k + l for k, l in zip(key, lock)]
        if all(p <= 5 for p in pin_sum):
            nr_keys_that_fit += 1
    print(nr_keys_that_fit)