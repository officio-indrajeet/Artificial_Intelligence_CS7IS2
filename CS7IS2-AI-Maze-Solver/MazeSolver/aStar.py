from pyamaze import maze, agent, textLabel
from queue import PriorityQueue
import time


def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2

    return abs(x1-x2) + abs(y1-y2)


def aStar(m):
    start = (m.rows, m.cols)
    g_score = {cell: float('inf') for cell in m.grid}
    g_score[start] = 0
    f_score = {cell: float('inf') for cell in m.grid}
    f_score[start] = h(start, (1, 1))

    open = PriorityQueue()
    open.put((h(start, (1, 1)), h(start, (1, 1)), start))
    aPath = {}
    start_time = time.time()
    while not open.empty():
        currCell = open.get()[2]
        if currCell == (1, 1):
            break
        for d in 'ESNW':
            if m.maze_map[currCell][d] == True:
                if d == 'E':
                    childCell = (currCell[0], currCell[1]+1)
                if d == 'W':
                    childCell = (currCell[0], currCell[1]-1)
                if d == 'N':
                    childCell = (currCell[0]-1, currCell[1])
                if d == 'S':
                    childCell = (currCell[0]+1, currCell[1])

                temp_g_score = g_score[currCell]+1
                temp_f_score = temp_g_score+h(childCell, (1, 1))

                if temp_f_score < f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open.put((temp_f_score, h(childCell, (1, 1)), childCell))
                    aPath[childCell] = currCell
    end_time = time.time()
    fwdPath = {}
    cell = (1, 1)
    while cell != start:
        fwdPath[aPath[cell]] = cell
        cell = aPath[cell]
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
    path, time_taken = aStar(m)

    a = agent(m, footprints=True, shape='arrow')
    m.tracePath({a: path})
    l = textLabel(m, 'A Star Path Length', len(path)+1)
    print("Time taken by A* algorithm: {:.4f} seconds".format(time_taken))
    m.run()
