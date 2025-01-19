from collections import deque
MASK = 2**24 - 1

def simulate_secret(secret, iterations):
    for _ in range(iterations): secret = get_next_secret(secret)
    return secret

def process_price_sequences(secret, iterations, price_sequences):
    previous_price_diffs = deque(maxlen=4)
    taken_sequences = set()
    prev_price = secret % 10
    for _ in range(iterations):
        secret = get_next_secret(secret)
        price = secret % 10
        price_diff = price - prev_price

        previous_price_diffs.append(price_diff)

        if len(previous_price_diffs) > 3 and tuple(previous_price_diffs) not in taken_sequences:
            if tuple(previous_price_diffs) not in price_sequences: price_sequences[tuple(previous_price_diffs)] = 0
            price_sequences[tuple(previous_price_diffs)] += price
            taken_sequences.add(tuple(previous_price_diffs))
        prev_price = price
    return price_sequences

def get_next_secret(secret):
    secret = ((secret << 6) ^ secret) & MASK
    secret = ((secret >> 5) ^ secret) & MASK
    secret = ((secret << 11) ^ secret) & MASK
    return secret

if __name__ == '__main__':
    initial_secrets = [int(line) for line in open('input.in')]

    # Part 1
    print(sum(simulate_secret(secret, 2000) for secret in initial_secrets))

    # Part 2
    price_sequences = {}
    for secret in initial_secrets: process_price_sequences(secret, 2000, price_sequences)

    max_sequence = max(price_sequences, key=price_sequences.get)
    max_value = price_sequences[max_sequence]
    print(f"Max value: {max_value} from sequence: {max_sequence}")
