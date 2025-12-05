use std::usize;

fn main() -> Result<(), std::io::Error> {
    let mut paper_roll_diagram: Vec<Vec<char>> = std::fs::read_to_string("input.in")?
        .lines()
        .map(|a| a.chars().collect())
        .collect();

    let mut total_removed_rolls = 0;
    while {
        let mut removed_rolls = vec![];
        for i in 0..paper_roll_diagram.len() {
            for j in 0..paper_roll_diagram[i].len() {
                if at_roll(i,j, &paper_roll_diagram) 
                    && valid_roll(i, j, &paper_roll_diagram) 
                {
                    total_removed_rolls += 1;
                    removed_rolls.push((i,j));
                }
            }
        } 
        removed_rolls.iter().for_each(|(x,y)| {
            paper_roll_diagram[*x][*y] = '.';
        });

        !removed_rolls.is_empty()
    }{}

    println!("Total valid rolls found: {}", total_removed_rolls);
    Ok(())
}

fn at_roll(x: usize, y: usize, diagram: &Vec<Vec<char>>) -> bool {
    diagram[x][y] == '@'
}

fn valid_roll(x: usize, y: usize, diagram: &Vec<Vec<char>>) -> bool {
    let mut surrounding_rolls = 0;
    for dx in -1..=1 {
        for dy in -1..=1 {
            if dx == 0 && dy == 0 {
                continue;
            }
            let new_x = x as isize + dx;
            let new_y = y as isize + dy;

            if new_x >= 0 && new_x < diagram.len() as isize
                && new_y >= 0 && new_y < diagram[0].len() as isize
            {
                if diagram[new_x as usize][new_y as usize] == '@' {
                    surrounding_rolls += 1;
                }
            }
        }
    }

    surrounding_rolls < 4
}