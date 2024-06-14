import random
import time

def printBoard(board):
    print("\nTic Tac Toe Board:")
    print(" " + board[1] + " | " + board[2] + " | " + board[3] + " ")
    print("---+---+---")
    print(" " + board[4] + " | " + board[5] + " | " + board[6] + " ")
    print("---+---+---")
    print(" " + board[7] + " | " + board[8] + " | " + board[9] + " ")
    print()

def spaceIsFree(position):
    return board[position] == ' '

def insertLetter(letter, position):
    if spaceIsFree(position):
        board[position] = letter
        printBoard(board)
        if checkForWin():
            print(f"{letter} wins!")
            return True
        if checkDraw():
            print("Draw!")
            return True
    else:
        print("This space is occupied!")
    return False

def checkForWin():
    return (board[1] == board[2] == board[3] != ' ' or
            board[4] == board[5] == board[6] != ' ' or
            board[7] == board[8] == board[9] != ' ' or
            board[1] == board[4] == board[7] != ' ' or
            board[2] == board[5] == board[8] != ' ' or
            board[3] == board[6] == board[9] != ' ' or
            board[1] == board[5] == board[9] != ' ' or
            board[7] == board[5] == board[3] != ' ')

def checkDraw():
    return ' ' not in board.values()

def playerMove():
    position = int(input("Enter the position for 'O' (1-9): "))
    return insertLetter(player, position)

def compMove(first_move):
    global total_steps, total_time
    if first_move:
        position = random.choice([k for k in range(1, 10) if spaceIsFree(k)])
        return insertLetter(bot, position), 0, 1
    else:
        bestScore = -float('inf')
        bestMove = None
        count_calls = 0
        start_time = time.time()

        for key in board.keys():
            if spaceIsFree(key):
                board[key] = bot
                score, calls = minimax(board, 0, False, -float('inf'), float('inf'), 0) if use_alpha_beta else minimax(board, 0, False, 0)
                board[key] = ' '
                count_calls += calls
                if score > bestScore:
                    bestScore = score
                    bestMove = key

        elapsed_time = time.time() - start_time
        move_made = insertLetter(bot, bestMove)
        total_time += elapsed_time
        total_steps += count_calls
        return move_made, elapsed_time, count_calls

def minimax(board, depth, isMaximizing, alpha=None, beta=None, call_count=0):
    call_count += 1
    if checkForWin():
        return (1 if isMaximizing else -1), call_count
    if checkDraw():
        return 0, call_count

    if isMaximizing:
        bestScore = -float('inf')
        for key in board.keys():
            if spaceIsFree(key):
                board[key] = bot
                if use_alpha_beta:
                    score, count = minimaxAlphaBeta(board, depth + 1, False, alpha, beta, call_count)
                else:
                    score, count = minimax(board, depth + 1, False, call_count=call_count)
                board[key] = ' '
                bestScore = max(bestScore, score)
                call_count = count
                if use_alpha_beta and beta is not None:
                    alpha = max(alpha, bestScore)
                    if beta <= alpha:
                        break
        return bestScore, call_count
    else:
        bestScore = float('inf')
        for key in board.keys():
            if spaceIsFree(key):
                board[key] = player
                if use_alpha_beta:
                    score, count = minimaxAlphaBeta(board, depth + 1, True, alpha, beta, call_count)
                else:
                    score, count = minimax(board, depth + 1, True, call_count=call_count)
                board[key] = ' '
                bestScore = min(bestScore, score)
                call_count = count
                if use_alpha_beta and alpha is not None:
                    beta = min(beta, bestScore)
                    if beta <= alpha:
                        break
        return bestScore, call_count

def minimaxAlphaBeta(board, depth, isMaximizing, alpha, beta, call_count):
    return minimax(board, depth, isMaximizing, alpha, beta, call_count)

def chooseAlgorithm():
    global use_alpha_beta
    choice = input("Choose algorithm: 1 for Minimax, 2 for Alpha-Beta Pruning: ")
    use_alpha_beta = (choice == '2')

board = {i: ' ' for i in range(1, 10)}
player = 'O'
bot = 'X'
use_alpha_beta = False
total_time = 0
total_steps = 0
game_over = False
firstComputerMove = True

chooseAlgorithm()
printBoard(board)
print("Computer goes first! Good luck.")
print("Positions are as follow:")
print("1, 2, 3 ")
print("4, 5, 6 ")
print("7, 8, 9 ")
print("\n")

while not game_over:
    game_over, time_taken, steps_taken = compMove(firstComputerMove)
    firstComputerMove = False
    if not game_over:
        game_over = playerMove()

print(f"Total recursive steps taken: {total_steps}")
print(f"Total time taken: {total_time:.4f} seconds")
