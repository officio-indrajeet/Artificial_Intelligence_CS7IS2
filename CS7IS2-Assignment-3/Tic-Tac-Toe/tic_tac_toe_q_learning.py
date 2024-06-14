import random
import pickle
import time

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

def get_state(board):
    return "".join([board[i] if board[i] != ' ' else '0' for i in range(1, 10)])


def load_q_table(filename='q_table.pkl'):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}


def find_winning_move(board, player):
    for i in range(1, 10):
        if space_is_free(board, i):
            board[i] = player
            if check_for_win(board):
                board[i] = ' '
                return i
            board[i] = ' '
    return None


def minimax(board, depth, is_maximizing, player, opponent):
    if check_for_win(board):
        return -1 if is_maximizing else 1
    if check_draw(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(1, 10):
            if space_is_free(board, i):
                board[i] = opponent
                score = minimax(board, depth + 1, False, player, opponent)
                board[i] = ' '
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(1, 10):
            if space_is_free(board, i):
                board[i] = player
                score = minimax(board, depth + 1, True, player, opponent)
                board[i] = ' '
                best_score = min(score, best_score)
        return best_score


def best_move(board, player, opponent):
    best_val = -float('inf')
    move = None
    for i in range(1, 10):
        if space_is_free(board, i):
            board[i] = opponent
            move_val = minimax(board, 0, False, player, opponent)
            board[i] = ' '
            if move_val > best_val:
                best_val = move_val
                move = i
    return move


def save_q_table(q_table, filename='q_table.pkl'):
    with open(filename, 'wb') as f:
        pickle.dump(q_table, f)


def choose_action(board, q_table, epsilon=0.1):
    state = get_state(board)
    if random.random() < epsilon:  # Explore
        return random.choice([k for k in range(1, 10) if space_is_free(board, k)])
    else:  # Exploit
        all_q_values = q_table.get(state, {})
        if not all_q_values:
            return random.choice([k for k in range(1, 10) if space_is_free(board, k)])
        return max(all_q_values, key=all_q_values.get)


def update_q_table(q_table, state, action, reward, next_state, alpha=0.1, gamma=0.9):
    old_value = q_table.get(state, {}).get(action, 0)
    next_max = max(q_table.get(next_state, {}).values(), default=0)
    new_value = old_value + alpha * (reward + gamma * next_max - old_value)
    if state not in q_table:
        q_table[state] = {}
    q_table[state][action] = new_value


def player_move(board, q_table, player='X'):
    move = choose_action(board, q_table)
    board[move] = player
    print(f"Player {player} placed on position {move}")
    print_board(board)
    return move


def opponent_move(board, opponent='O', player='X'):
    win_move = find_winning_move(board, opponent)
    if win_move:
        board[win_move] = opponent
        print(f"Player {opponent} placed on winning position {win_move}")
        print_board(board)
        return win_move

    block_move = find_winning_move(board, player)
    if block_move:
        board[block_move] = opponent
        print(f"Player {opponent} blocks on position {block_move}")
        print_board(board)
        return block_move

    move = best_move(board, player, opponent)
    board[move] = opponent
    print(f"Player {opponent} plays on position {move} using minimax")
    print_board(board)
    return move


def main():
    board = {i: ' ' for i in range(1, 10)}
    q_table = load_q_table()
    player, opponent = 'X', 'O'
    print("Welcome to Tic Tac Toe!")
    print_board(board)

    total_steps = 0
    start_time = time.time()
    is_first_move_player = True
    is_first_move_opponent = True

    while True:
        if is_first_move_player:
            player_move_position = random.choice([i for i in range(1, 10) if space_is_free(board, i)])
            board[player_move_position] = player
            print(f"Player {player} makes a random first move on position {player_move_position}")
            is_first_move_player = False
        else:
            player_move_position = player_move(board, q_table, player)

        print_board(board)
        total_steps += 1
        if check_for_win(board):
            print(f"{player} wins!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break

        if is_first_move_opponent:
            opponent_move_position = random.choice([i for i in range(1, 10) if space_is_free(board, i)])
            board[opponent_move_position] = opponent
            print(f"Opponent {opponent} makes a random first move on position {opponent_move_position}")
            is_first_move_opponent = False
        else:
            opponent_move_position = opponent_move(board, opponent, player)

        print_board(board)
        total_steps += 1
        if check_for_win(board):
            print(f"{opponent} wins!")
            break
        elif check_draw(board):
            print("It's a draw!")
            break

    total_time = time.time() - start_time
    print(f"Total time taken: {total_time:.4f} seconds")
    print(f"Total steps taken: {total_steps} moves")

    save_q_table(q_table)


if __name__ == "__main__":
    main()

