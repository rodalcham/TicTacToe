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

	return None

def isGameOver(board, player1, player2):
	winner = check_winner(board)
	if winner == player1['symbol']:
		return 1
	if winner == player2['symbol']:
		return 2

	for row in board:
		for cell in row:
			if cell == ' ':
				return 0
	return 3

def printBoard():
	print(f"{board[0][0]} | {board[0][1]} | {board[0][2]}")
	print("---------")
	print(f"{board[1][0]} | {board[1][1]} | {board[1][2]}")
	print("---------")
	print(f"{board[2][0]} | {board[2][1]} | {board[2][2]}")

def registerInput(currentPlayer, board):
	while True:
		try:
			move = int(input(f"{currentPlayer['symbol']}'s turn. Choose a position (1-9): "))
		except ValueError:
			print("Invalid input! Enter a number 1-9.")
			continue 
		if move < 1 or move > 9:
			print("Number must be 1-9!")
			continue

		row = (move - 1) // 3
		col = (move - 1) % 3

		if board[row][col] == ' ':
			return (row, col)
		else:
			print("Spot already taken! Try again.")

import random

def genRandom(lowB, upB):
	return random.randrange(lowB, upB)

def displayResult(res):
	if res == 0:
		print("Game continues...")
	elif res == 1:
		print("Game Over: Player 1 wins!")
	elif res == 2:
		print("Game Over: Player 2 wins!")
	elif res == 3:
		print("Game Over: It's a draw!")

def startGame2p(player1, player2):
	current_turn = genRandom(1, 3)
	game_status = 0
	
	while game_status == 0:
		printBoard()
		
		if current_turn == 1:
			print("Player 1's turn")
			row, col = registerInput(player1, board)
			board[row][col] = player1['symbol']
			current_turn = 2
		else:
			print("Player 2's turn")
			row, col = registerInput(player2, board)
			board[row][col] = player2['symbol']
			current_turn = 1
			
		game_status = isGameOver(board, player1, player2)
	
	printBoard()
	displayResult(game_status)

# Run the game
if __name__ == "__main__":
	startGame2p(player1, player2)
