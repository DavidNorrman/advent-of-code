
def read_input(file):
    with open(file) as f:
        colors = f.readline().strip().split(', ')
        f.readline()
        towels = [line.strip() for line in f]
    return colors, towels

def color_scheme_is_possible(colors, towel, memo = {}):
    if towel in memo:
        return memo[towel]
    if not towel:
        return True
    
    for color in get_fitting_colors(colors, towel):
        if color_scheme_is_possible(colors, towel[len(color):], memo):
            memo[towel] = True
            return True
        
    memo[towel] = False
    return False

def color_combinations(colors, towel, memo = {}):
    if not towel:
        return 1
    if towel in memo:
        return memo[towel]
    count = sum(color_combinations(colors, towel[len(color):], memo) for color in get_fitting_colors(colors, towel))
    memo[towel] = count
    return count

def get_fitting_colors(colors, towel_colors):
    return (color for color in colors if towel_colors.startswith(color))

if __name__ == '__main__':
    colors, towels = read_input('input.in')
    # Part 1
    print(len([towel for towel in towels if color_scheme_is_possible(colors, towel)]))
    # Part 2
    print(sum(color_combinations(colors, towel) for towel in towels))
