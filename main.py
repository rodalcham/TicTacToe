board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]

player1 = {'turn': -1, 'symbol': ''}
player2 = {'turn': -1, 'symbol': ''}

# register user input
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

d