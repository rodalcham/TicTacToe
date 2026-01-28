board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]

player1 = {'turn': -1, 'symbol': ''}
player2 = {'turn': -1, 'symbol': ''}

# register user input
def registerInput(currentPlayer, board):
    move = int(input(f"{currentPlayer['symbol']}'s turn. Choose a position (1-9): "))
    print("You entered:", move)
