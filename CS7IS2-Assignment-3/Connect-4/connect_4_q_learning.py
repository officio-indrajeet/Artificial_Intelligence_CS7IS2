import random
import numpy as np
import pickle
import time
class QAgent:
    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.1):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0)

    def set_q_value(self, state, action, value):
        self.q_table[(state, action)] = value

    def choose_action(self, state, possible_actions):
        if random.random() < self.epsilon:
            return random.choice(possible_actions)
        else:
            q_values = [self.get_q_value(state, a) for a in possible_actions]
            max_q_value = max(q_values)
            actions_with_max_q_value = [a for a, q in zip(possible_actions, q_values) if q == max_q_value]
            return random.choice(actions_with_max_q_value)

    def learn(self, state, action, reward, next_state, possible_actions):
        current_q = self.get_q_value(state, action)
        max_future_q = max([self.get_q_value(next_state, a) for a in possible_actions], default=0)
        new_q = current_q + self.alpha * (reward + self.gamma * max_future_q - current_q)
        self.set_q_value(state, action, new_q)

    def save_q_table(self, file_path='q_table.pkl'):
        with open(file_path, 'wb') as file:
            pickle.dump(self.q_table, file)

    def load_q_table(self, file_path='q_table.pkl'):
        with open(file_path, 'rb') as file:
            self.q_table = pickle.load(file)

class Connect4:
    def __init__(self, rows, columns, start_player='X'):
        self.rows = rows
        self.columns = columns
        self.start_player = start_player
        self.reset()
        self.step_count = 0
        self.time_spent = 0

    def reset(self):
        self.board = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]
        self.turn = self.start_player

    def display_board(self):
        print("\n")
        for row in self.board:
            print('| ' + ' | '.join(row) + ' |')
        print('+---' * self.columns + '+')

    def get_state(self):
        return ''.join(sum(self.board, []))

    def insert_token(self, column):
        if column < 0 or column >= self.columns or self.board[0][column] != ' ':
            return False, self.get_state()
        for i in range(self.rows - 1, -1, -1):
            if self.board[i][column] == ' ':
                self.board[i][column] = self.turn
                return True, self.get_state()
        return False, self.get_state()

    def remove_token(self, column):
        # Remove the topmost token from the column
        for i in range(self.rows):
            if self.board[i][column] != ' ':
                self.board[i][column] = ' '
                break

    def check_winner(self):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(self.rows):
            for c in range(self.columns):
                if self.board[r][c] == ' ':
                    continue
                for dr, dc in directions:
                    line = []
                    for i in range(4):
                        rr, cc = r + dr * i, c + dc * i
                        if 0 <= rr < self.rows and 0 <= cc < self.columns and self.board[rr][cc] == self.turn:
                            line.append(self.board[rr][cc])
                        else:
                            break
                    if len(line) == 4:
                        return self.turn
        return None

    def switch_turn(self):
        self.turn = 'O' if self.turn == 'X' else 'X'

    def play_game(self, q_agent, start_player):
        self.start_player = start_player
        self.reset()
        game_over = False
        state = self.get_state()
        while not game_over:
            self.display_board()
            possible_actions = [i for i in range(self.columns) if self.board[0][i] == ' ']
            if not possible_actions:
                print("Draw!")
                break
            start_time = time.perf_counter()
            if self.turn == 'X':  # Q-learning agent
                action = q_agent.choose_action(state, possible_actions)
                print(f"Q-agent (X) chooses column {action}")
                _, new_state = self.insert_token(action)
                reward = 0
                if self.check_winner() == 'X':
                    reward = 1
                    game_over = True
                    print("Q-agent (X) wins!")
                elif not possible_actions:
                    reward = 0.5
                    game_over = True
                    print("Draw!")
                q_agent.learn(state, action, reward, new_state, possible_actions)
                state = new_state
            else:  # Default opponent random play
                action = self.intelligent_opponent_move()
                print(f"Default opponent (O) chooses column {action}")
                _, state = self.insert_token(action)
                if self.check_winner() == 'O':
                    reward = -1
                    game_over = True
                    print("Default Opponent (O) wins!")
            elapsed_time = time.perf_counter() - start_time
            self.time_spent += elapsed_time
            self.step_count += 1

            self.switch_turn()
        print(f"Total moves: {self.step_count}, Total time: {self.time_spent:.2f} seconds")

    def intelligent_opponent_move(self):
        # Prioritize winning moves and blocking moves
        for action in range(self.columns):
            if self.board[0][action] != ' ':  # Skip full columns
                continue
            _, _ = self.insert_token(action)
            if self.check_winner() == self.turn:  # Winning move
                self.remove_token(action)
                return action
            self.remove_token(action)

            self.switch_turn()
            _, _ = self.insert_token(action)
            if self.check_winner() == self.turn:  # Blocking move
                self.remove_token(action)
                self.switch_turn()
                return action
            self.remove_token(action)
            self.switch_turn()

        return random.choice([c for c in range(self.columns) if self.board[0][c] == ' '])

if __name__ == "__main__":
    print("Welcome to Connect 4 Q-Learning!")
    rows = int(input("Enter the number of rows for the board: "))
    columns = int(input("Enter the number of columns for the board: "))
    q_agent = QAgent()
    try:
        q_agent.load_q_table()
        print("Loaded existing Q-table.")
    except (FileNotFoundError, EOFError):
        print("No existing Q-table found, starting fresh.")

    while True:
        print("Who should start the game? \n1 for Default opponent\n2 for Q-agent")
        start_choice = input("Your choice: ")
        start_player = 'O' if start_choice == '1' else 'X'
        game = Connect4(rows, columns, start_player=start_player)
        game.play_game(q_agent, start_player)

        q_agent.save_q_table()  # Save progress after each game
        print("Q-table saved.")

        continue_playing = input("Play another game? (yes/no): ")
        if continue_playing.lower() != 'yes':
            break
