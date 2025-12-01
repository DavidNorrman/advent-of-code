

fn main() {
    let lines = include_str!("input.in").lines().collect::<Vec<&str>>();

    let _part_one_zeros = _part_one(&lines);
    println!("Number of zeros in part one: {}", _part_one_zeros);

    let _part_two_zeros = _part_two(&lines);
    println!("Number of zeros in part two: {}", _part_two_zeros);
}

fn _part_one(rotations: &Vec<&str>) -> i32 {
    let mut zeros = 0;
    let mut current_pos = 50;

    for line in rotations {
        let direction = &line[0..1];
        let amount = &line[1..].parse::<i32>().unwrap();

        match direction {
            "L" => {
                current_pos = (current_pos - amount).rem_euclid(100);
                if current_pos == 0 {
                    zeros += 1;
                }
            }
            "R" => {
                current_pos = (current_pos + amount) % 100;
                if current_pos == 0 {
                    zeros += 1;
                }
            }
            _ => {}
        }

    }

    zeros
}

fn _part_two(rotations: &Vec<&str>) -> i32 {
    let mut zeros = 0;
    let mut current_pos = 50;

    for line in rotations {
        let direction = &line[0..1];
        let amount = &line[1..].parse::<i32>().unwrap();

        match direction {
            "L" => {
                let mut to_add = (100 - (current_pos - amount)) / 100;
                if current_pos == 0 {to_add -= 1;}
                zeros += to_add;
                current_pos = (current_pos - amount).rem_euclid(100);
            }
            "R" => {
                zeros += (current_pos + amount) / 100;
                current_pos = (current_pos + amount) % 100;
            }
            _ => {}
        }
    }

    zeros
}