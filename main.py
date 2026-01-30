board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]

player1 = {'turn': -1, 'symbol': 'X'}
player2 = {'turn': -1, 'symbol': 'O'}

def check_winner(board):
    # Check rows
    for row in board:
        if row[0] != ' ' and row[0] == row[1] == row[2]:
            return row[0]

    # Check columns
    for col in range(3):
        if board[0][col] != ' ' and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]

    # Check diagonals
    if board[0][0] != ' ' and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    if board[0][2] != ' ' and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    # No winner
    return None

def isGameOver(board, player1, player2) :
	winner = check_winner(board)
	if winner == player1['symbol']:
		return 1 #player1 win
	if winner == player2['symbol']:
		return 2 #player2 win

	for row in board:
		for cell in row:
			if cell == ' ':
				return 0 #continue
	return 3 #draw

def printBoard():
    print(f"{board[0][0]} | {board[0][1]} | {board[0][2]}")
    print("---------")
    print(f"{board[1][0]} | {board[1][1]} | {board[1][2]}")
    print("---------")
    print(f"{board[2][0]} | {board[2][1]} | {board[2][2]}")	
    pass

#board[0][0] = 'X'
#board[0][1] = 'X'
#board[0][2] = 'X'
printBoard()
print(isGameOver(board, player1, player2))
