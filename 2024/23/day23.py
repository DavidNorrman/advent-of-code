from networkx import Graph, find_cliques
from itertools import combinations

if __name__ == '__main__':
    lan_network = Graph()
    [lan_network.add_edge(computer[0], computer[1]) for computer in (line.strip().split('-') for line in open('input.in'))]
    
    # Part 1
    t_triangles = set()
    for clique in find_cliques(lan_network):
        if len(clique) >= 3:
            for combination in combinations(clique, 3):
                if any(c.startswith('t') for c in combination):
                    t_triangles.add(tuple(sorted(combination)))
    print('Groups with a computer starting with t:', len(t_triangles))

    # Part 2
    largest_clique = max(find_cliques(lan_network), key=len)
    print('Password:', ','.join(sorted(largest_clique)))

    # Note:
    # The fact that I used networkx feels a bit like cheating, 
    # but I haven't used it before so I still learned something new.