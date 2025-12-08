use std::fs::read_to_string;
use union_find::{QuickUnionUf, UnionBySize, UnionFind};
use itertools::Itertools;

fn main() {
    let junction_coords: Vec<(i64, i64, i64)> = read_to_string("input.in")
        .unwrap_or_else(|e| panic!("{}", e))
        .lines()
        .map(|line| {
            let coords: Vec<i64> = line
                .split(',')
                .map(|num| num.parse::<i64>().expect("error parsing"))
                .collect();
            (coords[0], coords[1], coords[2])
        })
        .collect();
    
    let mut junction_distances: Vec<(usize, usize, f64)> = (0..junction_coords.len())
        .tuple_combinations()
        .map(|(i, j)| {
            let dist = straight_line_distance(junction_coords[i], junction_coords[j]);
            (i, j, dist)
        })
        .collect();
    junction_distances.sort_by(|a, b| a.2.partial_cmp(&b.2).unwrap());
    
    part_one(&junction_coords, &junction_distances);
    part_two(&junction_coords, &junction_distances);

}

fn part_one(coords: &[(i64, i64, i64)], distances: &[(usize, usize, f64)]) {
    let mut connections = QuickUnionUf::<UnionBySize>::new(coords.len());
    for (i, j, _) in distances.iter().take(1000) {
        connections.union(*i, *j);
    }
    
    let mut cluster_sizes= vec![0; coords.len()];
    for i in 0..coords.len() {
        let root = connections.find(i);
        cluster_sizes[root] += 1;
    }
    cluster_sizes.sort_by(|a, b| b.cmp(a));

    println!("Product of largest 3 cluster sizes: {}", 
        cluster_sizes.iter().take(3).product::<usize>()
    );
}

fn part_two(coords: &[(i64, i64, i64)], distances: &[(usize, usize, f64)]) {
    let mut connections = QuickUnionUf::<UnionBySize>::new(coords.len());
    let mut number_of_clusters = coords.len();

    for (i, j, _) in distances.iter() {
        if connections.find(*i) != connections.find(*j) {
            connections.union(*i, *j);
            number_of_clusters -= 1;
        }
        if number_of_clusters == 1 {
            println!("Final X coord product: {}", coords[*i].0 * coords[*j].0);
            break;
        }
    }
}

fn straight_line_distance(
    point1: (i64, i64, i64),
    point2: (i64, i64, i64),
) -> f64 {
    let dx = (point2.0 - point1.0) as f64;
    let dy = (point2.1 - point1.1) as f64;
    let dz = (point2.2 - point1.2) as f64;
    (dx * dx + dy * dy + dz * dz).sqrt()
}