import random
import time

depth_limit = 4
def print_board(board):
    print("\nTic Tac Toe Board:")
    print(" " + board[1] + " | " + board[2] + " | " + board[3] + " ")
    print("---+---+---")
    print(" " + board[4] + " | " + board[5] + " | " + board[6] + " ")
    print("---+---+---")
    print(" " + board[7] + " | " + board[8] + " | " + board[9] + " ")
    print()

def space_is_free(board, position):
    return board[position] == ' '

def insert_letter(board, letter, position):
    board[position] = letter
    print(f"{letter} places on position {position}")
    print_board(board)
    if check_draw(board):
        print("Draw!")
        return True  # Indicate game end
    if check_for_win(board):
        print(f"{letter} wins!")
        return True  # Indicate game end
    return False  # Game continues

def check_for_win(board):
    return (board[1] == board[2] == board[3] != ' ' or
            board[4] == board[5] == board[6] != ' ' or
            board[7] == board[8] == board[9] != ' ' or
            board[1] == board[4] == board[7] != ' ' or
            board[2] == board[5] == board[8] != ' ' or
            board[3] == board[6] == board[9] != ' ' or
            board[1] == board[5] == board[9] != ' ' or
            board[7] == board[5] == board[3] != ' ')

def check_draw(board):
    return ' ' not in board.values()

def find_winning_move(board, mark):
    for key in range(1, 10):
        if space_is_free(board, key):
            board[key] = mark
            if check_for_win(board):
                board[key] = ' '
                return key
            board[key] = ' '
    return None

def select_strategic_move(board):
    for key in [5, 1, 3, 7, 9, 2, 4, 6, 8]:  # Center, corners, then sides
        if space_is_free(board, key):
            return key

def opponent_move(board, player, opponent):
    # First, check if the opponent can win in the next move
    winning_move = find_winning_move(board, opponent)
    if winning_move is not None:
        insert_letter(board, opponent, winning_move)
        print(f"Opponent ({opponent}) plays winning move at position {winning_move}")
        return

    # Next, check if it needs to block the player from winning
    blocking_move = find_winning_move(board, player)
    if blocking_move is not None:
        insert_letter(board, opponent, blocking_move)
        print(f"Opponent ({opponent}) blocks player ({player}) at position {blocking_move}")
        return

    # If no immediate win or block is possible, use Minimax to determine the best move
    best_move = None
    best_score = float('inf')
    for key in range(1, 10):
        if space_is_free(board, key):
            board[key] = opponent
            score, _ = minimax(board, 0, True, opponent, player, -float('inf'), float('inf'), [0])
            board[key] = ' '
            if score < best_score:
                best_score = score
                best_move = key

    # Make the best move determined by Minimax if no direct win or block was available
    if best_move is not None:
        insert_letter(board, opponent, best_move)
        print(f"Opponent ({opponent}) makes a strategic move at position {best_move}")

def minimax(board, depth, is_maximizing, player, opponent, alpha, beta, count_calls):
    count_calls[0] += 1
    if depth == depth_limit or check_for_win(board) or check_draw(board):
        return evaluate_board(board, player, opponent, depth), count_calls[0]

    if check_for_win(board):
        return (1 if is_maximizing else -1), count_calls[0]
    if check_draw(board):
        return 0, count_calls[0]

    if is_maximizing:
        best_score = -float('inf')
        for key in range(1, 10):
            if space_is_free(board, key):
                board[key] = player
                score, calls = minimax(board, depth + 1, False, player, opponent, alpha, beta, count_calls)
                board[key] = ' '
                best_score = max(best_score, score)
                if alpha is not None and beta is not None:
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return best_score, count_calls[0]
    else:
        best_score = float('inf')
        for key in range(1, 10):
            if space_is_free(board, key):
                board[key] = opponent
                score, calls = minimax(board, depth + 1, True, player, opponent, alpha, beta, count_calls)
                board[key] = ' '
                best_score = min(best_score, score)
                if alpha is not None and beta is not None:
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return best_score, count_calls[0]
def evaluate_board(board, player, opponent, depth):
    if check_for_win(board):
        if board[next(iter(board))] == player:
            return 10 - depth
        else:
            return depth - 10
    return 0
def comp_move(board, player, opponent, use_alpha_beta, move_count):
    start_time = time.time()
    count_calls = [0]

    if move_count == 1:
        free_positions = [pos for pos in range(1, 10) if space_is_free(board, pos)]
        first_move = random.choice(free_positions)
        insert_letter(board, player, first_move)
    else:
        best_score = -float('inf')
        best_move = None
        for key in range(1, 10):
            if space_is_free(board, key):
                board[key] = player
                if use_alpha_beta:
                    score, calls = minimax(board, 0, False, player, opponent, -float('inf'), float('inf'), count_calls)
                else:
                    score, calls = minimax(board, 0, False, player, opponent, None, None, count_calls)
                board[key] = ' '
                if score > best_score:
                    best_score = score
                    best_move = key
                count_calls[0] += calls  # Accumulate total calls

        if best_move is not None:
            insert_letter(board, player, best_move)

    elapsed_time = time.time() - start_time
    return count_calls[0], elapsed_time



def main():
    board = {key: ' ' for key in range(1, 10)}
    player = 'X'  # Computer's marker
    opponent = 'O'  # Default AI opponent's marker
    use_alpha_beta = int(input("Choose algorithm for Computer 'X' (1 for Minimax, 2 for Alpha-Beta Pruning): ")) == 2
    total_steps = 0
    total_time = 0
    move_count = 1

    print("Welcome to Tic Tac Toe!")
    print_board(board)

    while True:
        if move_count % 2 != 0:
            print("Computer's move (X):")
            steps, time_taken = comp_move(board, player, opponent, use_alpha_beta, move_count)
            total_steps += steps
            total_time += time_taken
            if check_for_win(board) or check_draw(board):
                break  # Break the loop if the game is over
        else:
            print("Default Opponent's move (O):")
            steps, time_taken = comp_move(board, opponent, player, False, move_count)
            total_steps += steps
            total_time += time_taken
            if check_for_win(board) or check_draw(board):
                break  # Break the loop if the game is over
        move_count += 1

    print(f"Total recursive steps taken: {total_steps}")
    print(f"Total time taken: {total_time:.4f} seconds")

if __name__ == "__main__":
    main()
1
