import random
import copy


def move_vac(grid, vacpos, dir):
    new_x = vacpos[0] + dir[0]
    new_y = vacpos[1] + dir[1]

    if new_x < 0 or new_x > rg[len(rg)-1]:
        return False

    if new_y < 0 or new_y > rg[len(rg)-1]:
        return False

    curpos = grid[vacpos[0]][vacpos[1]]
    tarpos = grid[vacpos[0] + dir[0]][vacpos[1] + dir[1]]
    grid[vacpos[0]][vacpos[1]] = '_' if curpos == '@' else '*'
    grid[vacpos[0] + dir[0]][vacpos[1] + dir[1]] = '@' if tarpos == '_' else '&'
    return True


def print_grid(grid):
    for row in reversed(rg):
        print(str(row) + ' ' + ' '.join(str(grid[col][row]) for col in rg))
    print('  ' + ' '.join(str(num) for num in rg))

def animate_grid(grid):
    for row in reversed(rg):
        print('\n'.join(str(row) + ' ' + ' '.join(str(grid[row][col]) for col in rg)))
    print('  ' + ' '.join(str(num) for num in rg))

class SearchNode:
    def __init__(self, stat, vac, paren, act, cst):
        self.state = stat
        self.vacpos = vac   # not strictly necessary but saves us from having to search state
        self.parent = paren
        self.action = act
        self.cost = cst


rg = list(range(int(input("how big would you like the grid to be on a side\nint>"))))

# * dust
# _ empty
# & vac and dust
# @ vac and empty
world = [['*' if random.random() < 0.2 else '_' for col in rg] for row in rg]
world[0][0] = '@' if world[0][0] == '_' else '&'
print("world created, printing:")
print_grid(world)

root = SearchNode(copy.deepcopy(world), (0, 0), None, "", 0)
cur = root
queue = []

dirs = [((0, 1), "N"), ((1, 0), "E"), ((0, -1), "S"), ((-1, 0), "W")]
found = False
while not found:
    if any('*' in row for row in cur.state) or any('&' in row for row in cur.state):
        if cur.cost < 200:
            # suck
            modstate = copy.deepcopy(cur.state)
            if modstate[cur.vacpos[0]][cur.vacpos[1]] == '&':
                modstate[cur.vacpos[0]][cur.vacpos[1]] = '@'
                cur = SearchNode(modstate, cur.vacpos, cur, "Suck", cur.cost + 1)
                queue.clear()
                curpath = []
                it = copy.copy(cur)
                while it.action != "":
                    curpath.append(it)
                    it = it.parent
                #print("suck found, path is: " + ' '.join(node.action for node in reversed(curpath)))

            # moves
            for dir in dirs:
                modstate = copy.deepcopy(cur.state)
                if move_vac(modstate, cur.vacpos, dir[0]):
                    queue.append(SearchNode(modstate, (cur.vacpos[0] + dir[0][0], cur.vacpos[1] + dir[0][1]), cur, dir[1], cur.cost + 1))

        if len(queue) > 0:
            cur = queue.pop(0)
        else:
            print("no solution found in search space. final configuration:")
            print_grid(cur.state)
            break
    else:
        found = True

if found:
    solution = []
    it = copy.copy(cur)
    while it.action != "":
        solution.append(it)
        it = it.parent

    print("\naction solution order is:")
    for node in reversed(solution):
        print(node.action + ", ", end='')
    print()
    world[cur.parent.vacpos[0]][cur.parent.vacpos[1]] = '@'

    arrows = {'N': '^', 'E': '>', 'S': 'v', 'W': '<'}
    it = copy.copy(cur.parent)
    while it.action != '':
        if it.action != 'Suck':
            world[it.parent.vacpos[0]][it.parent.vacpos[1]] = arrows[it.action]
        it = it.parent
    print()
    print_grid(world)

    print("\n\na. The number of actions in the solution returned by the search.")
    print(str(len(solution)), end='\n\n')
    print("b. The total cost of the solution.")
    print(str(len(solution)), end='\n\n')
    print("c. The initial state of the environment.")
    print_grid(world)
    print("\nd. The state of the environment after each action is performed.")
    for node in reversed(solution):
        print("\naction: " + node.action)
        print_grid(node.state)
