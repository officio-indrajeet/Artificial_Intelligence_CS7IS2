from pyamaze import maze, agent, COLOR, textLabel
import time


def DFS(m):
    start = (m.rows, m.cols)
    explored = [start]
    frontier = [start]
    dfsPath = {}
    start_time = time.time()
    while len(frontier) > 0:
        currCell = frontier.pop()
        if currCell == (1, 1):
            break
        for d in 'ESNW':
            if m.maze_map[currCell][d] == True:
                if d == 'E':
                    childCell = (currCell[0], currCell[1]+1)
                elif d == 'W':
                    childCell = (currCell[0], currCell[1]-1)
                elif d == 'S':
                    childCell = (currCell[0]+1, currCell[1])
                elif d == 'N':
                    childCell = (currCell[0]-1, currCell[1])
                if childCell in explored:
                    continue
                explored.append(childCell)
                frontier.append(childCell)
                dfsPath[childCell] = currCell
    end_time = time.time()
    fwdPath = {}
    cell = (1, 1)
    while cell != start:
        fwdPath[dfsPath[cell]] = cell
        cell = dfsPath[cell]
    return fwdPath, end_time - start_time


if __name__ == '__main__':
    print("\nPlease select Maze: \n")
    print("1. 5x5 Maze")
    print("2. 10x10 Maze")
    print("3. 20x20 Maze")
    print("4. 30x30 Maze")
    print("5. 50x50 Maze")
    print("6. Custom Maze")

    maze_choice = input("\nEnter your choice : ")

    if maze_choice == '1':
        m = maze(5, 5)
    elif maze_choice == '2':
        m = maze(10, 10)
    elif maze_choice == '3':
        m = maze(20, 20)
    elif maze_choice == '4':
        m = maze(30, 30)
    elif maze_choice == '5':
        m = maze(50, 50)
    elif maze_choice == '6':
        rows = int(input("Enter number of rows for custom maze: "))
        cols = int(input("Enter number of columns for custom maze: "))
        m = maze(rows, cols)
    else:
        print("Invalid choice!")
        exit()

    m.CreateMaze()
    path, time_taken = DFS(m)  # Retrieve path and algorithm time
    a = agent(m, footprints=True, shape='arrow')
    m.tracePath({a: path})
    l = textLabel(m, 'DFS Path Length', len(path)+1)
    print("Time taken by DFS algorithm: {:.4f} seconds".format(time_taken))
    m.run()
