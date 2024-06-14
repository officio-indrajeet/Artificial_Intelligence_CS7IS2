from pyamaze import maze, agent, COLOR, textLabel
from MDP import ValueIteration


def main():
    print("\nPlease select Maze: \n")
    print("1. 5x5 Maze")
    print("2. 10x10 Maze")
    print("3. 20x20 Maze")
    print("4. 30x30 Maze")
    print("5. 50x50 Maze")
    print("6. Custom Maze")
    maze_choice = input("\nEnter your choice : ")

    if maze_choice == '1':
        rows, cols = 5, 5
    elif maze_choice == '2':
        rows, cols = 10, 10
    elif maze_choice == '3':
        rows, cols = 20, 20
    elif maze_choice == '4':
        rows, cols = 30, 30
    elif maze_choice == '5':
        rows, cols = 50, 50
    elif maze_choice == '6':
        rows = int(input("Enter number of rows for custom maze: "))
        cols = int(input("Enter number of columns for custom maze: "))
    else:
        print("Invalid choice!")
        exit()

    goal_x, goal_y = GOAL = 1, 1

    m = maze(rows=rows, cols=cols)
    m.CreateMaze(x=goal_x, y=goal_y, pattern=None,
                 theme=COLOR.dark, loopPercent=100)

    setDeterministic = True

    agents = [0, 0]

    pathVI = None
    pathPI = None

    trackVI = ValueIteration(m, GOAL, isDeterministic=setDeterministic)
    trackVI.calculate_valueIteration()

    v = agent(m, shape='arrow', footprints=True, color=COLOR.red)

    agents[0] = v

    pathVI, timeVI = trackVI.create_searchPath((rows, cols))

    totalVIPath = textLabel(m, f'Value Iteration Path', len(pathVI) + 1)
    totalVITime = textLabel(
        m, f'Value Iteration Time', round(timeVI * 1000, 4))

    tracingDict = {}
    for i, val in enumerate([pathVI, pathPI]):
        if val is not None:
            tracingDict[agents[i]] = val

    m.tracePath(tracingDict, delay=200)
    m.run()


if __name__ == '__main__':
    main()
