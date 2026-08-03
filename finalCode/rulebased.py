def displayBoard(board):
    print("---------------------")
    
    for i in range(5):
        print("| ", end="")
        
        for j in range(5):
            print(board[i][j], end=" | ")
        
        print()
    
    print("---------------------")

def equality(x, y, z, l):
    if x==y and y==z and z==l and l!=' ':
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

    # ==========L===========
#    ---------------------
#   | X | O |   |   |   | 
#   | S | X | O |   |   | 
#   |   | S | X | O |   | 
#   |   |   | S | X | O | 
#   |   |   |   | S |(X)| 
#   ---------------------
    if equality(board[0][0], board[1][1], board[2][2], board[3][3]):
        return 4 if board[0][0] == 'X' else -4
    if equality(board[1][1], board[2][2], board[3][3], board[4][4]):
        return 4 if board[1][1] == 'X' else -4
    # =====================
    if equality(board[0][1], board[1][2], board[2][3], board[3][4]):
        return 4 if board[0][1] == 'X' else -4
    if equality(board[1][0], board[2][1], board[3][2], board[4][3]):
        return 4 if board[1][0] == 'X' else -4
    # =====================

    # =========R============
#   ---------------------
#   |   |   |   | O | X | 
#   |   |   | O | X | S | 
#   |   | O | X | S |   | 
#   | O | X | S |   |   | 
#   |(X)| S |   |   |   | 
#   ---------------------
    if equality(board[0][4], board[1][3], board[2][2], board[3][1]):
        return 4 if board[0][4] == 'X' else -4
    if equality(board[1][3], board[2][2], board[3][1], board[4][0]):
        return 4 if board[2][2] == 'X' else -4
    # =====================
    if equality(board[0][3], board[1][2], board[2][1], board[3][0]):
        return 4 if board[0][3] == 'X' else -4
    if equality(board[1][4], board[2][3], board[3][2], board[4][1]):
        return 4 if board[1][4] == 'X' else -4
    # =====================


    tie = True
    for i in range(5):
         for j in range(5):
             if board[i][j] == ' ':
                 tie = False
    return 1 if tie else 0


#******************Rule-Based Agent************************
import random

#************RULES*************
#1-Win moves
#2-Block opponent
#3-Create fork
#4-Center move
#5-Corner move
#6-Random move

def get_valid_moves(board):
    moves=[]
    for i in range(5):
        for j in range (5):
            if board[i][j]==' ':
                moves.append((i,j))
    return moves

#1-Win moves
def win_move(board,player):
    moves=get_valid_moves(board)
    for move in moves:
        r,c=move
        board[r][c]=player
        result=checkWinner(board)
        if(player=='X' and result==4) or (player=='O' and result==-4):
            board[r][c]=" "
            return move
        board[r][c]=" "
    return None

#2-Block opponent
def block_opponent(board,player):
    opponent='O' if player=='X' else'X'
    block=win_move(board,opponent)
    return block

#3-Create fork
def fork_move(board,player):
    moves=get_valid_moves(board)
    
    for move in moves:
        r,c=move
        board[r][c]=player
        winning_chance=0
        next_moves=get_valid_moves(board)
        
        for next_move in next_moves:
            nr,nc=next_move
            board[nr][nc]=player
            result = checkWinner(board)
            
            board[nr][nc]=' '
            if(player=='X' and result==4) or (player=='O' and result==-4):#    88/7489248929898256+555555=====/*********
                winning_chance+=1
        
        board[r][c]=' '
        if winning_chance>=2:
            return move
    return None

#4-Center move
def center_move(board):
    if board[2][2]==' ':
        return(2,2)
    return None

#5-Corner move
def corner_move(board):
    corner=[(0,0),(4,4),(0,4),(4,0)]
    for r,c in corner:
        if board[r][c]==' ':
            return(r,c)
    return None

#6-Random move
def random_move(board):
    moves=get_valid_moves(board)
    return random.choice(moves)

#************************************************
def rule_based_agent(board,player):
    #1-win
    move=win_move(board,player)
    if move:
        return move
    
    #2-block opponent
    move=block_opponent(board,player)
    if move:
        return move

    #3-create fork
    move=fork_move(board,player)
    if move:
        return move

    #4-center
    move=center_move(board)
    if move:
        return move
    
    #5-corner
    move=corner_move(board)
    if move:
        return move

    #6-random
    return random_move(board)
#***************************************************
if __name__ == "__main__":

    board = [
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' '],
    ]

    displayBoard(board)

    row, clm = 0, 0
    winned = False
    player = 'X'

    while not winned:

        if player == 'X':
            row = int(input("Enter the row.........."))
            clm = int(input("Enter the column.........."))
        else:
            row, clm = rule_based_agent(board, 'O')
            print(f"AI played: ({row}, {clm})")

        if row > 4 or row < 0 or clm > 4 or clm < 0 or board[row][clm] != ' ':
            print("try this again in a valid place\n")
            continue

        board[row][clm] = player = ('X' if player == 'O' else 'O')

        displayBoard(board)

        winned = checkWinner(board)

    if checkWinner(board) == 1:
        print("Tie!")
    else:
        print(f"player *{' X ' if checkWinner(board) == 4 else ' O '}* is the winner")