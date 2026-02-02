import random


def computerTurn(board, difficulty='easy', computer_symbol='O', player_symbol='X'):
    available_positions = getAvailablePositions(board)

    if difficulty == 'easy':
        return random.choice(available_positions)
    elif difficulty == 'hard':
        return smartMove(board, available_positions, computer_symbol, player_symbol)


def getAvailablePositions(board):
    available = []
    position = 1

    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                available.append(position)
            position = position + 1

    return available


def smartMove(board, available_positions, computer_symbol, player_symbol):
    moves_made = 9 - len(available_positions)
    is_going_first = isComputerGoingFirst(board, computer_symbol)

    for pos in available_positions:
        if isWinningMove(board, pos, computer_symbol):
            return pos

    for pos in available_positions:
        if isWinningMove(board, pos, player_symbol):
            return pos

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

    if moves_made == 0:
        corners = [1, 3, 7, 9]
        return random.choice(corners)

    if moves_made == 1:
        return respondToOpening(board, available_positions, computer_symbol, player_symbol)

    if moves_made == 2 and is_going_first:
        return executeCornerForkStrategy(board, available_positions, computer_symbol)

    if 5 in available_positions:
        return 5

    opposite_corner = getOppositeCornerOfOpponent(board, available_positions, player_symbol)
    if opposite_corner:
        return opposite_corner

    corners = [1, 3, 7, 9]
    for corner in corners:
        if corner in available_positions:
            return corner

    edges = [2, 4, 6, 8]
    for edge in edges:
        if edge in available_positions:
            return edge

    return available_positions[0]


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


def isWinningMove(board, position, symbol):
    row = (position - 1) // 3
    col = (position - 1) % 3

    original = board[row][col]

    board[row][col] = symbol

    won = checkWinCondition(board, symbol)

    board[row][col] = original

    return won


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