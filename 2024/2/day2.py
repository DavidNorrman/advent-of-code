VERBOSE = False


def ingest_input(input_file_path):
    reports = []

    with open(input_file_path, 'r') as file:
        for line in file:
            report = line.split()
            report = list(map(int, report))
            reports.append(report)
    return reports


def count_safe_reports(reports, allow_dampener=False):
    safe_reports = 0

    for report in reports:
        if report_is_safe(report, allow_dampener):
            safe_reports += 1
    return safe_reports


def report_is_safe(report, allow_dampener=False):
    if VERBOSE:
        print(f"Checking report: {report}")
        print(f"Checking report: {report}")
    strictly_increasing = (
        check_and_dampen(report, allow_dampener, is_strictly_increasing)
    )
    strictly_decreasing = (
        check_and_dampen(report, allow_dampener, is_strictly_decreasing)
    )

    if VERBOSE:
        print(f"increasing: {strictly_increasing}")
        print(f"decreasing: {strictly_decreasing}")
    return strictly_increasing or strictly_decreasing


def check_and_dampen(report, allow_dampener, logic):
    is_safe, faulty_index = check_report(report, logic)

    if not allow_dampener:
        return is_safe
    else:
        new_report_a = report[:faulty_index] + report[faulty_index + 1:]
        new_report_b = report[:faulty_index + 1] + report[faulty_index + 2:]

        is_safe_a, _ = check_report(new_report_a, logic)
        is_safe_b, _ = check_report(new_report_b, logic)
        return is_safe_a or is_safe_b


def check_report(report, logic):
    faulty_index = -1
    for i in range(len(report) - 1):
        if not logic(report[i], report[i + 1]):
            faulty_index = i
            return False, faulty_index
    return True, faulty_index


def is_strictly_increasing(level_a, level_b):
    return not (
        level_a > level_b
        or level_a < level_b - 3
        or level_a == level_b
    )


def is_strictly_decreasing(level_a, level_b):
    return not (
        level_a < level_b
        or level_a > level_b + 3
        or level_a == level_b
    )


if __name__ == '__main__':
    reports = ingest_input('input.in')
    # print(reports)

    safe_reports = count_safe_reports(reports, True)
    print(safe_reports)
