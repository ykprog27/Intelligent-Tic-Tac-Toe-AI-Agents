from rulebased import rule_based_agent
from minmax import minimax_agent
from minmax import checkWinner
from qlearning import learning_agent
import numpy as np
# =========================================
# WRAPPER FOR Q-LEARNING AGENT
# =========================================
def q_agent_wrapper(board, player):

    # convert board to numpy array
    np_board = np.array(board)

    # convert spaces to '-'
    np_board[np_board == ' '] = '-'

    # call q-learning agent
    move = learning_agent(np_board, player)

    return move
# =========================================
def create_board():
    return [
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
    ]
# =========================================

def play_game(agent_x, agent_o):
    board = create_board()
    player = 'X'
    while True:
        # ===== PLAYER X =====
        if player == 'X':

            row, col = agent_x(board, 'X')

            # safety check
            if board[row][col] != ' ':
                return 'O'

        # ===== PLAYER O =====
        else:

            row, col = agent_o(board, 'O')

            # safety check
            if board[row][col] != ' ':
                return 'X'

        # make move
        board[row][col] = player

        # check result
        result = checkWinner(board)

        if result == 4:
            return 'X'

        elif result == -4:
            return 'O'

        elif result == 1:
            return 'Draw'

        # switch player
        player = 'O' if player == 'X' else 'X'

# =========================================

def update_elo(ratingA, ratingB, scoreA, k=32):

    expectedA = 1 / (1 + 10 ** ((ratingB - ratingA) / 400))

    newA = ratingA + k * (scoreA - expectedA)

    return round(newA)

# =========================================

def run_tournament(agent1, name1, agent2, name2, games=10):

    wins1 = 0
    wins2 = 0
    draws = 0

    elo1 = 1000
    elo2 = 1000

    for i in range(games):

        # alternate starting player
        if i % 2 == 0:

            result = play_game(agent1, agent2)

            if result == 'X':

                wins1 += 1

                elo1 = update_elo(elo1, elo2, 1)
                elo2 = update_elo(elo2, elo1, 0)

            elif result == 'O':

                wins2 += 1

                elo1 = update_elo(elo1, elo2, 0)
                elo2 = update_elo(elo2, elo1, 1)

            else:

                draws += 1

                elo1 = update_elo(elo1, elo2, 0.5)
                elo2 = update_elo(elo2, elo1, 0.5)

        else:

            result = play_game(agent2, agent1)

            if result == 'X':

                wins2 += 1

                elo2 = update_elo(elo2, elo1, 1)
                elo1 = update_elo(elo1, elo2, 0)

            elif result == 'O':

                wins1 += 1

                elo2 = update_elo(elo2, elo1, 0)
                elo1 = update_elo(elo1, elo2, 1)

            else:

                draws += 1

                elo1 = update_elo(elo1, elo2, 0.5)
                elo2 = update_elo(elo2, elo1, 0.5)

        print(f"Game {i+1} finished")

    # =====================================

    print("\n===================================")
    print(f"{name1} VS {name2}")
    print("===================================")

    print(f"{name1} Wins : {wins1}")
    print(f"{name2} Wins : {wins2}")
    print(f"Draws       : {draws}")

    print("\n========== WIN RATES ==========")

    print(f"{name1} Win Rate : {(wins1/games)*100:.2f}%")
    print(f"{name2} Win Rate : {(wins2/games)*100:.2f}%")
    print(f"Draw Rate         : {(draws/games)*100:.2f}%")

    print("\n========== ELO RATINGS ==========")

    print(f"{name1} ELO : {elo1}")
    print(f"{name2} ELO : {elo2}")

# =========================================

run_tournament(minimax_agent,"Minimax Agent",rule_based_agent,"Rule-Based Agent",games=10)
run_tournament(
    minimax_agent,
    "Minimax Agent",
    q_agent_wrapper,
    "Q-Learning Agent",
    games=10
)
run_tournament(
    rule_based_agent,
    "Rule-Based Agent",
    q_agent_wrapper,
    "Q-Learning Agent",
    games=10
)