
fn main() -> Result<(), Box<dyn std::error::Error>> {
    let id_vector = std::fs::read_to_string("input.in")?
        .split(',')
        .flat_map(|s| {
            let (start, end) = s.split_once('-').unwrap();
            (start.parse::<i64>().unwrap()..=end.parse::<i64>().unwrap()).collect::<Vec<i64>>()
        })
        .collect::<Vec<i64>>();

    let invalid_sum_part_one: i64 = id_vector
        .iter()
        .filter(|id| _first_part_filter(id))
        .sum::<i64>();

    let invalid_sum_part_two: i64 = id_vector
        .iter()
        .filter(|id| _second_part_filter(id))
        .sum::<i64>();

    println!("Invalid sum part one: {}", invalid_sum_part_one);
    println!("Invalid sum part two: {}", invalid_sum_part_two);
    Ok(())
}

fn _first_part_filter(id: &i64) -> bool {
    let id_length = id.to_string().len();
    let first_half = &id.to_string()[..id_length / 2];
    let second_half = &id.to_string()[id_length / 2..];
    first_half == second_half
}

fn _second_part_filter(id: &i64) -> bool {
    let id_string = id.to_string();
    let id_length = id_string.len();

    (2..=id_length)
        .filter(|i| id_length % i == 0)
        .map(|divisor| {
            let part_length = id_length / divisor;
            let parts: Vec<i32> = (0..divisor)
                .map(|i| id_string[i * part_length..(i + 1) * part_length].parse().unwrap())
                .collect();
            parts
        })
        .any(|parts| parts.windows(2).all(|w| w[0] == w[1]))
}