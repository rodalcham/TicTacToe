import random

# ==========================================
# REMOVE AFTER TESTING - START
# ==========================================
import tkinter as tk
from tkinter import messagebox

# Global variables for GUI (temporary for testing)
_ttt_win = None
_ttt_buttons = None
_ttt_status = None
_game_state = None
# ==========================================
# REMOVE AFTER TESTING - END
# ==========================================


def computerTurn(board, difficulty='easy', computer_symbol='O', player_symbol='X'):
    """
    Main function - Computer chooses its move

    Parameters:
        board: The game board (3x3 grid)
        difficulty: 'easy' or 'hard'
        computer_symbol: What the computer plays as ('X' or 'O')
        player_symbol: What the human plays as ('X' or 'O')

    Returns:
        A number from 1-9 representing the computer's move
    """
    # Get list of empty positions
    available_positions = getAvailablePositions(board)

    # Easy mode: just pick randomly
    if difficulty == 'easy':
        return random.choice(available_positions)

    # Hard mode: use smart strategy
    elif difficulty == 'hard':
        return smartMove(board, available_positions, computer_symbol, player_symbol)


def getAvailablePositions(board):
    """
    Find all empty spots on the board

    Returns: List of numbers 1-9 for empty positions
    """
    available = []
    position = 1

    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                available.append(position)
            position = position + 1

    return available


def smartMove(board, available_positions, computer_symbol, player_symbol):
    """
    Smart AI strategy - tries to win or force a draw
    """
    # Count how many moves have been made
    moves_made = 9 - len(available_positions)

    # Check if computer is going first or second
    is_going_first = isComputerGoingFirst(board, computer_symbol)

    # ==================================
    # PRIORITY 1: WIN THE GAME
    # ==================================
    for pos in available_positions:
        if isWinningMove(board, pos, computer_symbol):
            return pos

    # ==================================
    # PRIORITY 2: BLOCK OPPONENT'S WIN
    # ==================================
    for pos in available_positions:
        if isWinningMove(board, pos, player_symbol):
            return pos

    # ==================================
    # PRIORITY 3 & 4: DEPENDS ON POSITION
    # ==================================
    if is_going_first:
        # ATTACKING: Create fork first, then block

        # Priority 3: Try to create a fork (two winning threats)
        fork_move = findForkMove(board, available_positions, computer_symbol)
        if fork_move:
            return fork_move

        # Priority 4: Block opponent's fork
        opponent_fork = findForkMove(board, available_positions, player_symbol)
        if opponent_fork:
            # Try to force them to block us instead
            forcing_move = findForcingMove(board, available_positions, computer_symbol, player_symbol)
            if forcing_move:
                return forcing_move
            return opponent_fork

    else:
        # DEFENDING: Block fork first, then create

        # Priority 3: Block opponent's fork
        opponent_fork = findForkMove(board, available_positions, player_symbol)
        if opponent_fork:
            # Try to force them to block us instead
            forcing_move = findForcingMove(board, available_positions, computer_symbol, player_symbol)
            if forcing_move:
                return forcing_move
            return opponent_fork

        # Priority 4: Try to create our own fork
        fork_move = findForkMove(board, available_positions, computer_symbol)
        if fork_move:
            return fork_move

    # ==================================
    # SPECIAL FIRST MOVES
    # ==================================
    if moves_made == 0:
        # Very first move: pick a corner (best strategy)
        corners = [1, 3, 7, 9]
        return random.choice(corners)

    if moves_made == 1:
        # Second move overall: respond smartly to opponent
        return respondToOpening(board, available_positions, computer_symbol, player_symbol)

    if moves_made == 2 and is_going_first:
        # Third move: execute corner fork strategy
        return executeCornerForkStrategy(board, available_positions, computer_symbol)

    # ==================================
    # GENERAL GOOD MOVES
    # ==================================
    # Take center if available
    if 5 in available_positions:
        return 5

    # Take opposite corner of opponent
    opposite_corner = getOppositeCornerOfOpponent(board, available_positions, player_symbol)
    if opposite_corner:
        return opposite_corner

    # Take any corner
    corners = [1, 3, 7, 9]
    for corner in corners:
        if corner in available_positions:
            return corner

    # Take any remaining spot
    return available_positions[0]


def isComputerGoingFirst(board, computer_symbol):
    """
    Check if computer made the first move in the game
    """
    # Count computer's marks
    computer_count = 0
    for row in range(3):
        for col in range(3):
            if board[row][col] == computer_symbol:
                computer_count = computer_count + 1

    # Count player's marks
    player_symbol = 'X' if computer_symbol == 'O' else 'O'
    player_count = 0
    for row in range(3):
        for col in range(3):
            if board[row][col] == player_symbol:
                player_count = player_count + 1

    # Computer went first if it has same or more marks
    return computer_count >= player_count


def respondToOpening(board, available_positions, computer_symbol, player_symbol):
    """
    Smart response to opponent's first move
    """
    corners = [1, 3, 7, 9]

    # Find where opponent played
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

    # If opponent took a corner, take opposite corner
    if opponent_position in corners:
        opposite = getOppositeCorner(opponent_position)
        if opposite in available_positions:
            return opposite
        # If opposite taken, take center
        if 5 in available_positions:
            return 5

    # If opponent took center, take any corner
    if opponent_position == 5:
        for corner in corners:
            if corner in available_positions:
                return corner

    # If opponent took edge, take center
    if 5 in available_positions:
        return 5

    # Fallback: any corner
    for corner in corners:
        if corner in available_positions:
            return corner

    return available_positions[0]


def executeCornerForkStrategy(board, available_positions, computer_symbol):
    """
    Try to create a winning fork using corners
    """
    corners = [1, 3, 7, 9]
    corner_positions = {
        1: (0, 0),
        3: (0, 2),
        7: (2, 0),
        9: (2, 2)
    }

    # Find which corner we played first
    first_corner = None
    for corner in corners:
        row, col = corner_positions[corner]
        if board[row][col] == computer_symbol:
            first_corner = corner
            break

    if not first_corner:
        return available_positions[0]

    # Try opposite corner (best for fork)
    opposite = getOppositeCorner(first_corner)
    if opposite in available_positions:
        return opposite

    # Try other corners
    for corner in corners:
        if corner != first_corner and corner in available_positions:
            return corner

    return available_positions[0]


def getOppositeCorner(corner):
    """
    Get the diagonal opposite corner
    1 ↔ 9, 3 ↔ 7
    """
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
    """
    Find if opponent is in a corner, return opposite corner if available
    """
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
    """
    Find a move that creates TWO winning threats at once
    (This is the key to winning tic-tac-toe!)
    """
    for pos in available_positions:
        # Try placing symbol at this position
        row = (pos - 1) // 3
        col = (pos - 1) % 3
        board[row][col] = symbol

        # Count how many ways we could win next turn
        winning_threats = 0
        temp_available = getAvailablePositions(board)

        for next_pos in temp_available:
            if isWinningMove(board, next_pos, symbol):
                winning_threats = winning_threats + 1

        # Undo the test move
        board[row][col] = ' '

        # If we found 2+ winning threats, this is a fork!
        if winning_threats >= 2:
            return pos

    return None


def findForcingMove(board, available_positions, computer_symbol, player_symbol):
    """
    Find a move that threatens a win, forcing opponent to block
    instead of completing their fork
    """
    for pos in available_positions:
        # Try placing symbol
        row = (pos - 1) // 3
        col = (pos - 1) % 3
        board[row][col] = computer_symbol

        # Count winning threats this creates
        temp_available = getAvailablePositions(board)
        winning_threats = 0

        for next_pos in temp_available:
            if isWinningMove(board, next_pos, computer_symbol):
                winning_threats = winning_threats + 1

        # Undo test move
        board[row][col] = ' '

        # If creates exactly one threat (not fork), use it to force opponent
        if winning_threats == 1:
            return pos

    return None


def isWinningMove(board, position, symbol):
    """
    Check if placing symbol at position wins the game
    """
    # Convert position (1-9) to row, col (0-2)
    row = (position - 1) // 3
    col = (position - 1) % 3

    # Remember what was there
    original = board[row][col]

    # Try the move
    board[row][col] = symbol

    # Check if it wins
    won = checkWinCondition(board, symbol)

    # Undo the move
    board[row][col] = original

    return won


# ==========================================
# REMOVE AFTER TESTING - START
# (Your team will provide these functions)
# ==========================================
def checkWinCondition(board, symbol):
    """Check if the given symbol has won"""
    # Check all 3 rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == symbol:
            return True

    # Check all 3 columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == symbol:
            return True

    # Check diagonal top-left to bottom-right
    if board[0][0] == board[1][1] == board[2][2] == symbol:
        return True

    # Check diagonal top-right to bottom-left
    if board[0][2] == board[1][1] == board[2][0] == symbol:
        return True

    return False


def isGameOver(board):
    """Check if game is over. Returns: 0 (continue), 1 (X won), 2 (O won), 3 (draw)"""
    if checkWinCondition(board, 'X'):
        return 1
    if checkWinCondition(board, 'O'):
        return 2
    if len(getAvailablePositions(board)) == 0:
        return 3
    return 0


def onButtonClick(row, col):
    """Handle button click for player move"""
    global _game_state

    if _game_state['game_over']:
        return

    board = _game_state['board']

    # Check if position is available
    if board[row][col] != ' ':
        return

    # Player makes move
    player_symbol = _game_state['player_symbol']
    board[row][col] = player_symbol
    updateBoard()

    # Check if game over
    result = isGameOver(board)
    if result != 0:
        handleGameOver(result)
        return

    # Computer's turn
    _ttt_status.config(text=f"Computer's turn ({_game_state['computer_symbol']})...")
    _ttt_win.update()

    # Disable buttons during computer's turn
    for r in range(3):
        for c in range(3):
            _ttt_buttons[r][c]['state'] = 'disabled'

    # Small delay so player can see the board
    _ttt_win.after(500, makeComputerMove)


def makeComputerMove():
    """Execute computer's move"""
    global _game_state

    board = _game_state['board']

    position = computerTurn(board, _game_state['difficulty'],
                           _game_state['computer_symbol'],
                           _game_state['player_symbol'])

    row = (position - 1) // 3
    col = (position - 1) % 3
    board[row][col] = _game_state['computer_symbol']

    updateBoard()

    # Check if game over
    result = isGameOver(board)
    if result != 0:
        handleGameOver(result)
        return

    # Re-enable buttons for player's turn
    for r in range(3):
        for c in range(3):
            if board[r][c] == ' ':
                _ttt_buttons[r][c]['state'] = 'normal'

    _ttt_status.config(text=f"Your turn ({_game_state['player_symbol']})")


def updateBoard():
    """Update the GUI board display"""
    global _game_state
    board = _game_state['board']

    for r in range(3):
        for c in range(3):
            cell = board[r][c]
            if cell == ' ':
                _ttt_buttons[r][c]['text'] = ''
                _ttt_buttons[r][c]['fg'] = 'gray'
            else:
                _ttt_buttons[r][c]['text'] = cell
                _ttt_buttons[r][c]['fg'] = 'blue' if cell == 'X' else 'red'

    _ttt_win.update()


def handleGameOver(result):
    """Handle end of game"""
    global _game_state
    _game_state['game_over'] = True

    # Disable all buttons
    for r in range(3):
        for c in range(3):
            _ttt_buttons[r][c]['state'] = 'disabled'

    computer_first = _game_state['computer_first']

    if result == 1:
        if computer_first:
            message = "😔 Computer Wins! (X)\nBetter luck next time!"
        else:
            message = "🎉 You Win! (X)\nCongratulations!"
    elif result == 2:
        if computer_first:
            message = "🎉 You Win! (O)\nCongratulations!"
        else:
            message = "😔 Computer Wins! (O)\nBetter luck next time!"
    else:
        message = "🤝 It's a Draw!\nWell played!"

    _ttt_status.config(text=message.split('\n')[0])

    # Ask to play again
    _ttt_win.after(1000, lambda: askPlayAgain(message))


def askPlayAgain(message):
    """Ask if player wants to play again"""
    play_again = messagebox.askyesno("Game Over", message + "\n\nPlay again?")
    if play_again:
        startNewGame()
    else:
        _ttt_win.destroy()


def startNewGame():
    """Reset the game for a new round"""
    global _game_state

    # Keep difficulty, randomize who goes first
    difficulty = _game_state['difficulty']
    computer_first = random.choice([True, False])

    _game_state = {
        'board': [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
        'difficulty': difficulty,
        'computer_first': computer_first,
        'player_symbol': 'O' if computer_first else 'X',
        'computer_symbol': 'X' if computer_first else 'O',
        'game_over': False
    }

    # Reset buttons
    for r in range(3):
        for c in range(3):
            _ttt_buttons[r][c]['text'] = ''
            _ttt_buttons[r][c]['state'] = 'normal'

    if computer_first:
        _ttt_status.config(text=f"Computer goes first! You are {_game_state['player_symbol']}")
        # Disable buttons and make computer move
        for r in range(3):
            for c in range(3):
                _ttt_buttons[r][c]['state'] = 'disabled'
        _ttt_win.after(1000, makeComputerMove)
    else:
        _ttt_status.config(text=f"You go first! You are {_game_state['player_symbol']}")


def createGUI(difficulty='hard'):
    """Create the Tkinter GUI"""
    global _ttt_win, _ttt_buttons, _ttt_status, _game_state

    computer_first = random.choice([True, False])

    _game_state = {
        'board': [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']],
        'difficulty': difficulty,
        'computer_first': computer_first,
        'player_symbol': 'O' if computer_first else 'X',
        'computer_symbol': 'X' if computer_first else 'O',
        'game_over': False
    }

    _ttt_win = tk.Tk()
    _ttt_win.title(f"Tic-Tac-Toe - {difficulty.upper()} Mode")
    _ttt_win.resizable(False, False)

    # Create buttons
    _ttt_buttons = [[None for _ in range(3)] for _ in range(3)]

    for r in range(3):
        for c in range(3):
            btn = tk.Button(_ttt_win, text='', font=('Helvetica', 40, 'bold'),
                          width=4, height=2, bg='white',
                          command=lambda row=r, col=c: onButtonClick(row, col))
            btn.grid(row=r, column=c, padx=5, pady=5)
            _ttt_buttons[r][c] = btn

    # Status label
    if computer_first:
        status_text = f"Computer goes first! You are {_game_state['player_symbol']}"
    else:
        status_text = f"You go first! You are {_game_state['player_symbol']}"

    _ttt_status = tk.Label(_ttt_win, text=status_text,
                          font=('Helvetica', 14), pady=10)
    _ttt_status.grid(row=3, column=0, columnspan=3)

    # New Game button
    new_game_btn = tk.Button(_ttt_win, text="New Game", font=('Helvetica', 12),
                            command=startNewGame, bg='lightblue')
    new_game_btn.grid(row=4, column=0, columnspan=3, pady=5)

    # If computer goes first, make its move after window appears
    if computer_first:
        for r in range(3):
            for c in range(3):
                _ttt_buttons[r][c]['state'] = 'disabled'
        _ttt_win.after(1000, makeComputerMove)

    _ttt_win.mainloop()


def testGame():
    """Start the game with difficulty selection"""
    # Create difficulty selection window
    root = tk.Tk()
    root.title("Tic-Tac-Toe - Select Difficulty")
    root.geometry("300x200")
    root.resizable(False, False)

    tk.Label(root, text="Select Difficulty", font=('Helvetica', 16, 'bold')).pack(pady=20)

    def start_easy():
        root.destroy()
        createGUI('easy')

    def start_hard():
        root.destroy()
        createGUI('hard')

    tk.Button(root, text="Easy (Random moves)", font=('Helvetica', 12),
             command=start_easy, width=20, bg='lightgreen').pack(pady=10)

    tk.Button(root, text="Hard (Optimal strategy)", font=('Helvetica', 12),
             command=start_hard, width=20, bg='lightcoral').pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    testGame()
# ==========================================
# REMOVE AFTER TESTING - END
# ==========================================