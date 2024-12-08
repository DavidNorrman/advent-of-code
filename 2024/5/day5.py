import functools

def read_input(input_file_path):
    rules_map = {}
    page_updates = []

    input_section = 'rules'
    with open(input_file_path, 'r') as file:
        for line in file:
            if input_section == 'rules':
                if line.strip() == '':
                    input_section = 'updates'
                else:
                    page, next_page = line.strip().split('|')
                    page = int(page)
                    next_page = int(next_page)
                    if page not in rules_map:
                        rules_map[page] = []
                    rules_map[page].append(next_page)
            else:
                update_numbers = [int(x) for x in line.strip().split(',')]
                page_updates.append(update_numbers)

    return rules_map, page_updates


def get_page_update_lists_control_sum(page_updates,
                                      rules_map,
                                      correct_wrong_orders=False):
    middle_page_sum = 0

    for page_update_list in page_updates:
        update_is_valid = validate_update(page_update_list, rules_map)

        if update_is_valid and not correct_wrong_orders:
            middle_page_sum += page_update_list[len(page_update_list) // 2]
        elif not update_is_valid and correct_wrong_orders:
            corrected_update = sorted(
                page_update_list,
                key=functools.cmp_to_key(lambda a, b: compare_pages(a, b, rules_map))
            )
            # print(f"Corrected update: {corrected_update}")
            # print(f"it is valid: {validate_update(corrected_update, rules_map)}")
            middle_page_sum += corrected_update[len(corrected_update) // 2]

    return middle_page_sum


def validate_update(page_update_list, rules_map):
    for i in range(len(page_update_list) - 1):
        if not check_page_is_after(page_update_list[i], page_update_list[i + 1], rules_map):
            return False
    return True


def check_page_is_after(page, next_page, rules_map):
    if page in rules_map:
        return next_page in rules_map[page]
    return False


def compare_pages(a, b, rules_map):
    if check_page_is_after(a, b, rules_map):
        return -1
    elif check_page_is_after(b, a, rules_map):
        return 1
    else:
        return 0


if __name__ == '__main__':
    rules_map, page_updates = read_input('./input.in')

    # print(rules_map)
    # print(page_updates)

    print("Part 1:")
    control_sum = get_page_update_lists_control_sum(page_updates, rules_map)
    print(control_sum)

    print("Part 2:")
    corrected_control_sum = get_page_update_lists_control_sum(
        page_updates,
        rules_map,
        correct_wrong_orders=True
    )
    print(corrected_control_sum)
