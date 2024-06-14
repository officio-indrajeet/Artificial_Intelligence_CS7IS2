import random
import time

class Connect4:
    def __init__(self, rows, columns, ai_with_pruning, ai_starts):
        self.rows = rows
        self.columns = columns
        self.board = [[' ' for _ in range(columns)] for _ in range(rows)]
        self.ai_with_pruning = ai_with_pruning
        self.turn = 'O' if ai_starts else 'X'
        self.total_steps = 0
        self.total_time = 0
        self.first_move = True
        self.computer_wins = 0

    def display_board(self):
        print("\n")
        for row in self.board:
            print('| ' + ' | '.join(row) + ' |')
        print('+---' * self.columns + '+')

    def insert_token(self, column):
        if column < 0 or column >= self.columns or self.board[0][column] != ' ':
            return False, -1
        for i in range(self.rows - 1, -1, -1):
            if self.board[i][column] == ' ':
                self.board[i][column] = self.turn
                return True, i
        return False, -1

    def remove_token(self, column):
        for i in range(self.rows):
            if self.board[i][column] != ' ':
                self.board[i][column] = ' '
                break

    def check_winner(self, check_turn=None):
        check_turn = check_turn or self.turn
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(self.rows):
            for c in range(self.columns):
                if self.board[r][c] != check_turn:
                    continue
                for dr, dc in directions:
                    line = []
                    for i in range(4):
                        rr, cc = r + dr * i, c + dc * i
                        if 0 <= rr < self.rows and 0 <= cc < self.columns and self.board[rr][cc] == check_turn:
                            line.append(self.board[rr][cc])
                        else:
                            break
                    if len(line) == 4:
                        return check_turn
        return None

    def switch_turn(self):
        self.turn = 'O' if self.turn == 'X' else 'X'

    def evaluate_board(self):
        winner = self.check_winner()
        if winner == 'O':
            return 1
        elif winner == 'X':
            return -1
        return 0

    def is_full(self):
        return all(self.board[0][c] != ' ' for c in range(self.columns))

    def minimax(self, depth, maximizingPlayer, alpha=None, beta=None):
        self.total_steps += 1
        if depth == 0 or self.check_winner() or self.is_full():
            return self.evaluate_board()

        if maximizingPlayer:
            maxEval = float('-inf')
            for c in range(self.columns):
                if self.board[0][c] == ' ':
                    _, row = self.insert_token(c)
                    self.switch_turn()
                    start_time = time.time()
                    eval = self.minimax(depth - 1, False, alpha, beta)
                    elapsed = time.time() - start_time
                    self.total_time += elapsed
                    self.board[row][c] = ' '
                    self.switch_turn()
                    maxEval = max(maxEval, eval)
                    if self.ai_with_pruning:
                        if alpha is not None and beta is not None:
                            alpha = max(alpha, eval)
                            if beta <= alpha:
                                break
            return maxEval
        else:
            minEval = float('inf')
            for c in range(self.columns):
                if self.board[0][c] == ' ':
                    _, row = self.insert_token(c)
                    self.switch_turn()
                    start_time = time.time()
                    eval = self.minimax(depth - 1, True, alpha, beta)
                    elapsed = time.time() - start_time
                    self.total_time += elapsed
                    self.board[row][c] = ' '
                    self.switch_turn()
                    minEval = min(minEval, eval)
                    if self.ai_with_pruning:
                        if alpha is not None and beta is not None:
                            beta = min(beta, eval)
                            if beta <= alpha:
                                break
            return minEval

    def best_move(self, depth=4):
        best_score = float('-inf')
        best_column = None
        for c in range(self.columns):
            if self.board[0][c] == ' ':
                _, row = self.insert_token(c)
                self.switch_turn()
                start_time = time.time()
                score = self.minimax(depth - 1, False, float('-inf'), float('inf'))
                elapsed = time.time() - start_time
                self.total_time += elapsed
                self.board[row][c] = ' '
                self.switch_turn()
                if score > best_score:
                    best_score = score
                    best_column = c
        return best_column

    def opponent_move(self):
        col = self.best_move(depth=2)
        return col

    def play_game(self):
        while True:
            self.display_board()
            if self.turn == 'X':
                print("Player X (Default opponent) is making its move...")
                col = self.opponent_move()
            else:
                print("Computer is making its move...")
                if self.first_move:
                    col = random.choice([i for i in range(self.columns) if self.board[0][i] == ' '])
                    self.first_move = False
                else:
                    col = self.best_move()

            if col is None or not self.insert_token(col)[0]:
                print("Invalid move, try again.")
                continue

            winner = self.check_winner()
            if winner:
                self.display_board()
                print(f"Player {winner} wins!")
                if winner == 'O':
                    self.computer_wins += 1
                break
            elif self.is_full():
                self.display_board()
                print("It's a draw!")
                break
            self.switch_turn()
        print(f"Total steps taken: {self.total_steps}")
        print(f"Total time taken: {self.total_time:.2f} seconds")

# Game setup and initialization from user input
print("Welcome to Connect 4!")
rows = int(input("Please enter board size:\nRows: "))
cols = int(input("Columns: "))

print("Choose algorithm: \n1 for Minimax\n2 for Alpha-Beta Pruning")
algorithm_choice = input("Your choice: ")
pruning = algorithm_choice == '2'

print("Who should start the game? \n1 for Default opponent\n2 for Computer")
start_choice = input("Your choice: ")
ai_starts = start_choice == '2'

game = Connect4(rows, cols, ai_with_pruning=pruning, ai_starts=ai_starts)
game.play_game()

