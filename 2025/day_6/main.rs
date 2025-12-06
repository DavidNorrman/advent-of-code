fn main() -> Result<(), std::io::Error> {
    // Part One
    // _part_one();

    // Part Two
    let input: Vec<String> = std::fs::read_to_string("input.in")?
        .lines()
        .map(|s| s.to_string())
        .collect();

    let mut numbers_vector: Vec<Vec<usize>> = Vec::new();
    let mut current_numbers: Vec<usize> = Vec::new();
    
    let mut operators: Vec<char> = Vec::new();

    for j in (0..input[0].len()).rev() {
        let mut number_chars: Vec<char> = input
            .iter()
            .map(|line| line.chars().nth(j).unwrap())
            .collect();

        if number_chars.iter().all(|c| *c == ' ') {
            continue;
        }

        match number_chars[number_chars.len()-1] {
            '+' | '*' => {
                operators.push(number_chars.pop().unwrap());

                let number = parse_number(&number_chars);
                current_numbers.push(number);

                numbers_vector.push(current_numbers);
                current_numbers = Vec::new();
            },
            _ => {
                let number = parse_number(&number_chars);
                current_numbers.push(number);
            }
        }
    }

    let final_sum: usize = numbers_vector
        .into_iter()
        .zip(operators.iter())
        .map(|(nums, op)| {
            nums.into_iter().reduce(|n, m| {
                match op {
                    '+' => n + m,
                    '*' => n * m,
                    _ => panic!("Unknown operation: {}", op),
                }
            }).unwrap()
        })
        .sum();

    println!("Final Sum: {}", final_sum);
    Ok(())
}


fn _part_one() -> Result<(), std::io::Error> {
    let input: Vec<Vec<String>> = std::fs::read_to_string("input.in")?
        .lines()
        .map(|s| {
            s.split(' ')
            .map(|s| {
                s.to_string()
            })
            .filter(|s| !s.is_empty())
            .collect()
        })
        .collect();

    let num_calculations = input[0].len();
    let mut results: Vec<usize> = Vec::new();
    for j in 0..num_calculations {
        let mut numbers: Vec<usize> = Vec::new();
        
        for i in 0..input.len()-1 {
            numbers.push(input[i][j].parse::<usize>().unwrap());
        }

        let operation = &input[input.len()-1][j];
        results.push(numbers
            .into_iter()
            .reduce(|n, m| {
                match operation.as_str() {
                    "+" => n + m,
                    "*" => n * m,
                    _ => panic!("Unknown operation: {}", operation),
                }
            }).unwrap()
        );
    }

    println!("Final Output: {}", results.into_iter().sum::<usize>());
    Ok(())
}

fn parse_number(chars: &[char]) -> usize {
    chars.iter().collect::<String>().trim().parse().unwrap()
}