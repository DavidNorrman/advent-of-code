fn main() -> Result<(), std::io::Error>{
    // change to 2 for part 1
    let batteries_per_bank: usize = 12;

    let total_joltage: i64 = std::fs::read_to_string("input.in")?
        .split("\n")
        .map(|a| { 
            let battery_vector = a.chars().collect::<Vec<char>>();

            let mut batteries_collected: Vec<char> = [].to_vec();
            let mut prev_index: usize = 0;

            for b in 0..(batteries_per_bank) {
                let max_index = battery_vector.len() - (batteries_per_bank - b);
                let battery = battery_vector[prev_index..=max_index]
                    .iter()
                    .max()
                    .unwrap();

                batteries_collected.push(*battery);
            
                prev_index = battery_vector[prev_index..]
                    .iter()
                    .position(|&c| c == *battery)
                    .unwrap() + 1 + prev_index;
            }
            
            let joltage_string: String = batteries_collected.iter().collect();
            let joltage: i64 = joltage_string.parse().unwrap();
            joltage
        })
        .sum();

    println!("Total joltage: {:?}", total_joltage);
    Ok(())
}