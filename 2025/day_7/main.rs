fn main() -> Result<(), std::io::Error> {
    let input = std::fs::read_to_string("input.in")?;
    let input_lines: Vec<Vec<char>> = input
        .lines()
        .map(|l| l.chars().collect())
        .collect();
    
    let start_pos = input_lines[0].iter().position(|c| *c == 'S').unwrap();

    let mut manifold_diagram = input_lines.clone();
    let mut splits = 0; 
    fill_regular_manifold((0, start_pos), &mut manifold_diagram, &mut splits);
    println!("Total number of splits: {}", splits);
    
    let mut quantum_manifold_diagram = input_lines.clone();
    let mut timeline_construct = vec![vec![0; input_lines[0].len()]; input_lines.len()];
    timeline_construct[0][start_pos] = 1;
    fill_quantum_manifold(&mut quantum_manifold_diagram, &mut timeline_construct);
    let final_timelines_sum: usize = timeline_construct[input_lines.len() - 1].iter().sum();
    println!("Total number of timelines: {}", final_timelines_sum);
    Ok(())
}

// Recursive solution for part 1
fn fill_regular_manifold(current_pos: (usize, usize), manifold_diagram: &mut Vec<Vec<char>>, splits: &mut i64) {
    if current_pos.0 + 1 >= manifold_diagram.len() {
        return;
    }
    
    let lower_character = manifold_diagram[current_pos.0+1][current_pos.1];

    match lower_character {
        '.' => {
            manifold_diagram[current_pos.0 + 1][current_pos.1] = '|';
            fill_regular_manifold((current_pos.0 + 1, current_pos.1), manifold_diagram, splits);
        }
        '^' => {
            *splits += 1;
            manifold_diagram[current_pos.0 + 1][current_pos.1 - 1] = '|';
            manifold_diagram[current_pos.0 + 1][current_pos.1 + 1] = '|';
            fill_regular_manifold((current_pos.0 + 1, current_pos.1 - 1), manifold_diagram, splits);
            fill_regular_manifold((current_pos.0 + 1, current_pos.1 + 1), manifold_diagram, splits);
        }
        _ => {}
    }
}

// Iterative solution for part 2
fn fill_quantum_manifold(manifold_diagram: &mut Vec<Vec<char>>, timeline_construct: &mut Vec<Vec<usize>>) {
    for row in 1..manifold_diagram.len() {
        for col in 0..manifold_diagram[0].len() {
            if manifold_diagram[row][col] == '^' {
                continue;
            }

            let above_character = manifold_diagram[row-1][col];
            if above_character == '|' || above_character == 'S' {
                manifold_diagram[row][col] = '|';
                timeline_construct[row][col] += timeline_construct[row-1][col];
            }
            
            if col > 0 {
                let left_character = manifold_diagram[row][col-1];
                if left_character == '^' {
                    manifold_diagram[row][col] = '|';
                    timeline_construct[row][col] += timeline_construct[row-1][col-1];
                }
            }
            
            if col + 1 < manifold_diagram[0].len() {
                let right_character = manifold_diagram[row][col+1];
                if right_character == '^' {
                    manifold_diagram[row][col] = '|';
                    timeline_construct[row][col] += timeline_construct[row-1][col+1];
                }
            }
        }
    }
}