fn main() -> Result<(), std::io::Error> {
    let input: Vec<String> = std::fs::read_to_string("input.in")?
        .lines()
        .map(|line| line.to_string())
        .collect();

    let (ranges, ids) = input
        .split_at(
        input
                .iter()
                .position(|line| line.is_empty())
                .unwrap()
        );

    let mut fresh_id_ranges: Vec<(usize, usize)> = vec![];
    ranges
        .iter()
        .for_each(|line| {
            let (start, end) = line
                .split_at(line.find('-').unwrap());

            fresh_id_ranges.push((
                start.parse::<usize>().unwrap(),
                end[1..].parse::<usize>().unwrap()
            ));
        });
    merge_ranges(&mut fresh_id_ranges);

    let fresh_ids: usize = ids
        .iter()
        .skip(1)
        .map(|line| -> usize{
            let id = line.parse::<usize>().unwrap();
            for (start, end) in &fresh_id_ranges {
                if id >= *start && id <= *end {
                    return 1;
                }
            }
            0
        })
        .sum();

    let total_possible_fresh_ids: usize = fresh_id_ranges
        .iter()
        .map(|(start, end)| {
            end - start + 1
        })
        .sum();

    println!("Total fresh IDs: {}", fresh_ids);
    println!("Total possible fresh IDs: {}", total_possible_fresh_ids);
    Ok(())
}

fn merge_ranges(ranges: &mut Vec<(usize, usize)>) {
    while {
        let mut merged = false;
        for i in 0..ranges.len() {
            for j in (i+1)..ranges.len() {
                let (start_i, end_i) = ranges[i];
                let (start_j, end_j) = ranges[j];
                if start_j <= end_i && end_j >= start_i {
                    ranges[i] = (start_i.min(start_j), end_i.max(end_j));
                    ranges.remove(j);
                    merged = true;
                    break;
                }
            }
        }
        merged
    }{}
}