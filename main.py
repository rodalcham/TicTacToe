import random
# ============================================================================
# GAME BOARD AND STATE
# ============================================================================

board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]

player1 = {'turn': -1, 'symbol': 'X'}
player2 = {'turn': -1, 'symbol': 'O'}


# ============================================================================
# BOARD DISPLAY AND INPUT
# ============================================================================

def printBoard():3
    def get_cell_display(row, col):
        if board[row][col] == ' ':
            return str((row * 3) + col + 1)
        return board[row][col]

    print(f" {get_cell_display(0, 0)} | {get_cell_display(0, 1)} | {get_cell_display(0, 2)}")
    print("-----------")
    print(f" {get_cell_display(1, 0)} | {get_cell_display(1, 1)} | {get_cell_display(1, 2)}")
    print("-----------")
    print(f" {get_cell_display(2, 0)} | {get_cell_display(2, 1)} | {get_cell_display(2, 2)}")


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


# ============================================================================
# WIN CHECKING
# ============================================================================

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


def checkWinCondition(board, symbol):
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == symbol:
            return True

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == symbol:
            return True

    if board[0][0] == board[1][1] == board[2][2] == symbol:
        return True

    if board[0][2] == board[1][1] == board[2][0] == symbol:
        return True

    return False


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


# ============================================================================
# COMPUTER AI LOGIC
# ============================================================================

def getAvailablePositions(board):
    available = []
    position = 1

    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                available.append(position)
            position = position + 1

    return available


def isWinningMove(board, position, symbol):
    row = (position - 1) // 3
    col = (position - 1) % 3

    original = board[row][col]

    board[row][col] = symbol

    won = checkWinCondition(board, symbol)

    board[row][col] = original

    return won


def findForkMove(board, available_positions, symbol):
    for pos in available_positions:
        row = (pos - 1) // 3
        col = (pos - 1) % 3
        board[row][col] = symbol

        winning_threats = 0
        temp_available = getAvailablePositions(board)

        for next_pos in temp_available:
            if isWinningMove(board, next_pos, symbol):
                winning_threats = winning_threats + 1

        board[row][col] = ' '

        if winning_threats >= 2:
            return pos

    return None


def findForcingMove(board, available_positions, computer_symbol, player_symbol):
    for pos in available_positions:
        row = (pos - 1) // 3
        col = (pos - 1) % 3
        board[row][col] = computer_symbol

        temp_available = getAvailablePositions(board)
        winning_threats = 0

        for next_pos in temp_available:
            if isWinningMove(board, next_pos, computer_symbol):
                winning_threats = winning_threats + 1

        board[row][col] = ' '

        if winning_threats == 1:
            return pos

    return None


def isComputerGoingFirst(board, computer_symbol, player_symbol):
    computer_count = 0
    for row in range(3):
        for col in range(3):
            if board[row][col] == computer_symbol:
                computer_count = computer_count + 1

    player_count = 0
    for row in range(3):
        for col in range(3):
            if board[row][col] == player_symbol:
                player_count = player_count + 1

    return computer_count >= player_count


def getOppositeCorner(corner):
    if corner == 1:
        return 9
    elif corner == 9:
        return 1
    elif corner == 3:
        return 7
    elif corner == 7:
        return 3
    return None


def getOppositeCornerOfOpponent(board, available_positions, player_symbol):
    corner_positions = {
        1: (0, 0),
        3: (0, 2),
        7: (2, 0),
        9: (2, 2)
    }

    for corner, (row, col) in corner_positions.items():
        if board[row][col] == player_symbol:
            opposite = getOppositeCorner(corner)
            if opposite and opposite in available_positions:
                return opposite

    return None


def respondToOpening(board, available_positions, computer_symbol, player_symbol):
    corners = [1, 3, 7, 9]

    opponent_position = None
    position = 1
    for row in range(3):
        for col in range(3):
            if board[row][col] == player_symbol:
                opponent_position = position
                break
            position = position + 1
        if opponent_position:
            break

    if opponent_position in corners:
        opposite = getOppositeCorner(opponent_position)
        if opposite in available_positions:
            return opposite
        if 5 in available_positions:
            return 5

    if opponent_position == 5:
        for corner in corners:
            if corner in available_positions:
                return corner

    if 5 in available_positions:
        return 5

    for corner in corners:
        if corner in available_positions:
            return corner

    return available_positions[0]


def executeCornerForkStrategy(board, available_positions, computer_symbol):
    corners = [1, 3, 7, 9]
    corner_positions = {
        1: (0, 0),
        3: (0, 2),
        7: (2, 0),
        9: (2, 2)
    }

    first_corner = None
    for corner in corners:
        row, col = corner_positions[corner]
        if board[row][col] == computer_symbol:
            first_corner = corner
            break

    if not first_corner:
        return available_positions[0]

    opposite = getOppositeCorner(first_corner)
    if opposite in available_positions:
        return opposite

    for corner in corners:
        if corner != first_corner and corner in available_positions:
            return corner

    return available_positions[0]


def smartMove(board, available_positions, computer_symbol, player_symbol):
    moves_made = 9 - len(available_positions)
    is_going_first = isComputerGoingFirst(board, computer_symbol, player_symbol)

    # Win if possible
    for pos in available_positions:
        if isWinningMove(board, pos, computer_symbol):
            return pos

    # Block opponent's winning move
    for pos in available_positions:
        if isWinningMove(board, pos, player_symbol):
            return pos

    # Fork strategies
    if is_going_first:
        fork_move = findForkMove(board, available_positions, computer_symbol)
        if fork_move:
            return fork_move

        opponent_fork = findForkMove(board, available_positions, player_symbol)
        if opponent_fork:
            forcing_move = findForcingMove(board, available_positions, computer_symbol, player_symbol)
            if forcing_move:
                return forcing_move
            return opponent_fork

    else:
        opponent_fork = findForkMove(board, available_positions, player_symbol)
        if opponent_fork:
            forcing_move = findForcingMove(board, available_positions, computer_symbol, player_symbol)
            if forcing_move:
                return forcing_move
            return opponent_fork

        fork_move = findForkMove(board, available_positions, computer_symbol)
        if fork_move:
            return fork_move

    # Opening move strategy
    if moves_made == 0:
        corners = [1, 3, 7, 9]
        return random.choice(corners)

    if moves_made == 1:
        return respondToOpening(board, available_positions, computer_symbol, player_symbol)

    if moves_made == 2 and is_going_first:
        return executeCornerForkStrategy(board, available_positions, computer_symbol)

    # Take center if available
    if 5 in available_positions:
        return 5

    # Take opposite corner
    opposite_corner = getOppositeCornerOfOpponent(board, available_positions, player_symbol)
    if opposite_corner:
        return opposite_corner

    # Take any corner
    corners = [1, 3, 7, 9]
    for corner in corners:
        if corner in available_positions:
            return corner

    # Take any edge
    edges = [2, 4, 6, 8]
    for edge in edges:
        if edge in available_positions:
            return edge

    return available_positions[0]


def computerTurn(board, difficulty='easy', computer_symbol='O', player_symbol='X'):
    available_positions = getAvailablePositions(board)

    if difficulty == 'easy':
        return random.choice(available_positions)
    elif difficulty == 'hard':
        return smartMove(board, available_positions, computer_symbol, player_symbol)


# ============================================================================
# GAME MODES
# ============================================================================

def genRandom(lowB, upB):
    return random.randrange(lowB, upB)


def displayResult(res):
    print("\n")
    if res == 0:
        print("Game continues...")
    elif res == 1:
        print("Game Over: Player 1 wins!")
    elif res == 2:
        print("Game Over: Player 2 wins!")
    elif res == 3:
        print("Game Over: It's a draw!")


def resetBoard():
    global board
    board = [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']
    ]


def startGame2p(player1, player2):
    resetBoard()
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


def startGameVsComputer(player1, computer, difficulty='hard'):
    resetBoard()
    current_turn = genRandom(1, 3)
    game_status = 0

    print(f"\nStarting game vs Computer ({difficulty} mode)")
    print(f"You are {player1['symbol']}, Computer is {computer['symbol']}\n")

    while game_status == 0:
        printBoard()

        if current_turn == 1:
            print("Your turn")
            row, col = registerInput(player1, board)
            board[row][col] = player1['symbol']
            current_turn = 2
        else:
            print("Computer's turn...")
            position = computerTurn(board, difficulty, computer['symbol'], player1['symbol'])
            row = (position - 1) // 3
            col = (position - 1) % 3
            board[row][col] = computer['symbol']
            print(f"Computer chose position {position}")
            current_turn = 1

        game_status = isGameOver(board, player1, computer)

    printBoard()
    displayResult(game_status)


# ============================================================================
# MAIN MENU
# ============================================================================

def main():
    while True:
        print("\n" + "="*40)
        print("TIC-TAC-TOE GAME")
        print("="*40)
        print("1. Two Player Mode")
        print("2. Play vs Computer (Easy)")
        print("3. Play vs Computer (Hard)")
        print("4. Exit")
        print("="*40)

        try:
            choice = int(input("Choose an option (1-4): "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        if choice == 1:
            startGame2p(player1, player2)
        elif choice == 2:
            computer = {'turn': -1, 'symbol': 'O'}
            startGameVsComputer(player1, computer, difficulty='easy')
        elif choice == 3:
            computer = {'turn': -1, 'symbol': 'O'}
            startGameVsComputer(player1, computer, difficulty='hard')
        elif choice == 4:
            print("Thanks for playing!")
            break
        else:
            print("Invalid choice! Please choose 1-4.")


if __name__ == "__main__":
    main()