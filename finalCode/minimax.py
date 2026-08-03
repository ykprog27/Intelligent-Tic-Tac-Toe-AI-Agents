def displayBoard(board):
    print("---------------------")
    
    for i in range(5):
        print("| ", end="")
        
        for j in range(5):
            print(board[i][j], end=" | ")
        
        print()
    
    print("---------------------")

# minimax.py

def equality(x, y, z, l):
    if x == y and y == z and z == l and l != ' ':
        return True
    return False

def checkWinner(board):
    for r in range(5):
        if equality(board[r][0], board[r][1], board[r][2], board[r][3]):
             return 4 if board[r][0] == 'X' else -4
        elif equality(board[r][1], board[r][2], board[r][3], board[r][4]):
            return 4 if board[r][1] == 'X' else -4

    for c in range(5):
        if equality(board[0][c], board[1][c], board[2][c], board[3][c]):
             return 4 if board[0][c] == 'X' else -4
        elif equality(board[1][c], board[2][c], board[3][c], board[4][c]):
             return 4 if board[1][c] == 'X' else -4  

    if equality(board[0][0], board[1][1], board[2][2], board[3][3]):
        return 4 if board[0][0] == 'X' else -4
    if equality(board[1][1], board[2][2], board[3][3], board[4][4]):
        return 4 if board[1][1] == 'X' else -4

    if equality(board[0][1], board[1][2], board[2][3], board[3][4]):
        return 4 if board[0][1] == 'X' else -4
    if equality(board[1][0], board[2][1], board[3][2], board[4][3]):
        return 4 if board[1][0] == 'X' else -4

    if equality(board[0][4], board[1][3], board[2][2], board[3][1]):
        return 4 if board[0][4] == 'X' else -4
    if equality(board[1][3], board[2][2], board[3][1], board[4][0]):
        return 4 if board[2][2] == 'X' else -4

    if equality(board[0][3], board[1][2], board[2][1], board[3][0]):
        return 4 if board[0][3] == 'X' else -4
    if equality(board[1][4], board[2][3], board[3][2], board[4][1]):
        return 4 if board[1][4] == 'X' else -4

    tie = True
    for i in range(5):
         for j in range(5):
             if board[i][j] == ' ':
                 tie = False
    return 1 if tie else 0

def evaluateLine(a, b, c, d):
    line = [a, b, c, d]
    x = line.count('X')
    o = line.count('O')

    if x > 0 and o > 0:
        return 0

    if o == 0:
        if x == 4: return 10000
        if x == 3: return 100
        if x == 2: return 10
        if x == 1: return 1

    if x == 0:
        if o == 4: return -10000
        if o == 3: return -100
        if o == 2: return -10
        if o == 1: return -1

    return 0

def evaluate(board):
    score = 0
    for r in range(5):
        for c in range(2):
            score += evaluateLine(board[r][c], board[r][c+1], board[r][c+2], board[r][c+3])

    for c in range(5):
        for r in range(2):
            score += evaluateLine(board[r][c], board[r+1][c], board[r+2][c], board[r+3][c])

    for r in range(2):
        for c in range(2):
            score += evaluateLine(board[r][c], board[r+1][c+1], board[r+2][c+2], board[r+3][c+3])

    for r in range(2):
        for c in range(3, 5):
            score += evaluateLine(board[r][c], board[r+1][c-1], board[r+2][c-2], board[r+3][c-3])
    return score

def getMoves(board):
    moves = []
    for i in range(5):
        for j in range(5):
            if board[i][j] == ' ':
                moves.append((i, j))
    return moves

def miniMax(board, depth, isMaximizing, alpha, beta):
    result = checkWinner(board)
    if result == 4: return 4000
    if result == -4: return -4000
    if result == 1: return 0
    if depth == 0: return evaluate(board)

    moves = getMoves(board)

    if isMaximizing:
        best = float('-inf')
        for i, j in moves:
            board[i][j] = 'X'
            score = miniMax(board, depth - 1, False, alpha, beta)
            board[i][j] = ' '
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = float('inf')
        for i, j in moves:
            board[i][j] = 'O'
            score = miniMax(board, depth - 1, True, alpha, beta)
            board[i][j] = ' '
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best
    
def getBestMove(board, depth=3):
    bestScore = float('-inf')
    move = None
    for i in range(5):
        for j in range(5):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                score = miniMax(board, depth, False, float('-inf'), float('inf'))
                board[i][j] = ' '
                if score > bestScore:
                    bestScore = score
                    move = (i, j)
    return move

if __name__ == "__main__":
    
    test_board = [[' ' for _ in range(5)] for _ in range(5)]
    print("--- Terminal Test Mode ---")
    row = int(input("Enter row: "))
    col = int(input("Enter col: "))
    print(f"You selected: {row}, {col}")