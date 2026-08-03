# Enhanced Q-Learning 5x5 Tic-Tac-Toe
import numpy as np
import random
import pickle

# =====================================
# SETTINGS
# =====================================

BOARD_SIZE = 5
WIN_LENGTH = 4

players = ['X', 'O']

learning_rate = 0.1

discount_factor = 0.9

exploration_rate = 1.0
min_exploration_rate = 0.01
exploration_decay = 0.995

num_episodes = 10000

WIN_REWARD = 100
LOSE_REWARD = -100
DRAW_REWARD = 10
MOVE_PENALTY = -1
BLOCK_REWARD = 5
THREE_IN_ROW_REWARD = 8

Q = {}

# =====================================
# CREATE BOARD
# =====================================


def create_board():
    return np.full((BOARD_SIZE, BOARD_SIZE), '-')


# =====================================
# PRINT BOARD
# =====================================


def print_board(board):
    print()

    for row in board:
        print(' | '.join(row))
        print('-' * (BOARD_SIZE * 4 - 1))

    print()


# =====================================
# BOARD TO STRING
# =====================================


def board_to_string(board):
    return ''.join(board.flatten())


# =====================================
# GET EMPTY CELLS
# =====================================


def get_empty_cells(board):
    return [tuple(cell) for cell in np.argwhere(board == '-')]


# =====================================
# CHECK WINNER
# =====================================


def check_winner(board, player):

    # Rows
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE - WIN_LENGTH + 1):

            segment = board[row, col:col + WIN_LENGTH]

            if all(cell == player for cell in segment):
                return True

    # Columns
    for col in range(BOARD_SIZE):
        for row in range(BOARD_SIZE - WIN_LENGTH + 1):

            segment = board[row:row + WIN_LENGTH, col]

            if all(cell == player for cell in segment):
                return True

    # Main Diagonal
    for row in range(BOARD_SIZE - WIN_LENGTH + 1):
        for col in range(BOARD_SIZE - WIN_LENGTH + 1):

            segment = [board[row + i][col + i] for i in range(WIN_LENGTH)]

            if all(cell == player for cell in segment):
                return True

    # Anti Diagonal
    for row in range(BOARD_SIZE - WIN_LENGTH + 1):
        for col in range(WIN_LENGTH - 1, BOARD_SIZE):

            segment = [board[row + i][col - i] for i in range(WIN_LENGTH)]

            if all(cell == player for cell in segment):
                return True

    return False


# =====================================
# GAME OVER
# =====================================


def is_game_over(board):

    if check_winner(board, 'X'):
        return True, 'X'

    if check_winner(board, 'O'):
        return True, 'O'

    if '-' not in board:
        return True, 'draw'

    return False, None


# =====================================
# HEURISTIC REWARDS
# =====================================


def count_consecutive(board, player, length):
    count = 0

    # Rows
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE - length + 1):

            segment = board[row, col:col + length]

            if np.count_nonzero(segment == player) == length:
                count += 1

    # Columns
    for col in range(BOARD_SIZE):
        for row in range(BOARD_SIZE - length + 1):

            segment = board[row:row + length, col]

            if np.count_nonzero(segment == player) == length:
                count += 1

    return count


# =====================================
# GET REWARD
# =====================================


def get_reward(board, player, winner):

    opponent = 'O' if player == 'X' else 'X'

    if winner == player:
        return WIN_REWARD

    if winner == opponent:
        return LOSE_REWARD

    if winner == 'draw':
        return DRAW_REWARD

    reward = MOVE_PENALTY

    player_threes = count_consecutive(board, player, 3)
    opponent_threes = count_consecutive(board, opponent, 3)

    reward += player_threes * THREE_IN_ROW_REWARD
    reward += opponent_threes * BLOCK_REWARD

    return reward


# =====================================
# CHOOSE ACTION
# =====================================


def choose_action(board, player, exploration_rate):

    state = board_to_string(board)

    empty_cells = get_empty_cells(board)

    # Exploration
    if random.uniform(0, 1) < exploration_rate or state not in Q:

        # Prefer center positions sometimes
        center = BOARD_SIZE // 2

        preferred_moves = []

        for cell in empty_cells:
            r, c = cell

            distance = abs(r - center) + abs(c - center)

            if distance <= 2:
                preferred_moves.append(cell)

        if preferred_moves:
            return random.choice(preferred_moves)

        return random.choice(empty_cells)

    # Exploitation
    q_values = Q[state]

    best_value = -float('inf')
    best_moves = []

    for cell in empty_cells:

        value = q_values[cell[0], cell[1]]

        if value > best_value:
            best_value = value
            best_moves = [cell]

        elif value == best_value:
            best_moves.append(cell)

    return random.choice(best_moves)


# =====================================
# UPDATE Q TABLE
# =====================================


def update_q_table(state, action, reward, next_state):

    if state not in Q:
        Q[state] = np.zeros((BOARD_SIZE, BOARD_SIZE))

    if next_state not in Q:
        Q[next_state] = np.zeros((BOARD_SIZE, BOARD_SIZE))

    current_q = Q[state][action[0], action[1]]

    max_future_q = np.max(Q[next_state])

    # Q Learning Equation
    new_q = current_q + learning_rate * (
            reward + discount_factor * max_future_q - current_q
    )

    Q[state][action[0], action[1]] = new_q


# =====================================
# TRAINING
# =====================================


agent_x_wins = 0
agent_o_wins = 0
draws = 0

for episode in range(num_episodes):

    board = create_board()

    current_player = random.choice(players)

    game_over = False

    while not game_over:

        state = board_to_string(board)

        action = choose_action(board, current_player, exploration_rate)

        row, col = action

        board[row, col] = current_player

        game_over, winner = is_game_over(board)

        next_state = board_to_string(board)

        reward = get_reward(board, current_player, winner)

        update_q_table(state, action, reward, next_state)

        if game_over:

            if winner == 'X':
                agent_x_wins += 1

            elif winner == 'O':
                agent_o_wins += 1

            else:
                draws += 1

        else:
            current_player = 'O' if current_player == 'X' else 'X'

    exploration_rate = max(
        min_exploration_rate,
        exploration_rate * exploration_decay
    )

    if (episode + 1) % 5000 == 0:
        print(f"Episode {episode + 1}/{num_episodes}")
        print(f"Exploration Rate: {exploration_rate:.4f}")
        print()


# =====================================
# SAVE Q TABLE
# =====================================


with open('q_table_5x5.pkl', 'wb') as file:
    pickle.dump(Q, file)

print("Training completed and Q-table saved.")


# =====================================
# TRAINING RESULTS
# =====================================


total_games = agent_x_wins + agent_o_wins + draws

print("========== TRAINING RESULTS ==========")
print(f"Total Games : {total_games}")
print(f"X Wins      : {agent_x_wins}")
print(f"O Wins      : {agent_o_wins}")
print(f"Draws       : {draws}")
print()

print(f"X Win Rate  : {(agent_x_wins / total_games) * 100:.2f}%")
print(f"O Win Rate  : {(agent_o_wins / total_games) * 100:.2f}%")
print(f"Draw Rate   : {(draws / total_games) * 100:.2f}%")


# =====================================
# HUMAN VS AGENT
# =====================================

with open('q_table_5x5.pkl', 'rb') as file:
    Q = pickle.load(file)
    
def learning_agent(board, player):

    np_board = np.array(board)

    np_board[np_board == ' '] = '-'

    state = board_to_string(np_board)

    empty_cells = get_empty_cells(np_board)

    if state not in Q:

        return random.choice(empty_cells)

    q_values = Q[state]

    best_value = -float('inf')
    best_moves = []

    for cell in empty_cells:

        value = q_values[cell[0], cell[1]]

        if value > best_value:

            best_value = value
            best_moves = [cell]

        elif value == best_value:

            best_moves.append(cell)

    return random.choice(best_moves)

if __name__ == "__main__":

    print("\n========== PLAY AGAINST AI ==========")

    board = create_board()

    human = 'X'
    ai = 'O'

    current_player = 'X'

    game_over = False

    while not game_over:

        print_board(board)

        if current_player == human:

            while True:

                try:
                    row = int(input(f"Enter row (0-{BOARD_SIZE - 1}): "))
                    col = int(input(f"Enter col (0-{BOARD_SIZE - 1}): "))

                    if board[row, col] == '-':
                        break

                    print("Cell already occupied!")

                except:
                    print("Invalid input!")

            action = (row, col)

        else:

            action = choose_action(board, ai, 0)

            print(f"AI chose: {action}")

        row, col = action

        board[row, col] = current_player

        game_over, winner = is_game_over(board)

        if game_over:

            print_board(board)

            if winner == human:
                print("You Win!")

            elif winner == ai:
                print("AI Wins!")

            else:
                print("Draw!")

        else:
            current_player = 'O' if current_player == 'X' else 'X'