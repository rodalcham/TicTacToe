def startGame2p(player1, player2):
    # 1. Decide who starts (using Rodrigo's genRandom)
    current_turn = genRandom(1, 2)
    game_status = 0 # 0 means the game is ongoing
    
    while game_status == 0:
        printBoard() # Fabian's function
        
        if current_turn == 1:
            print("Player 1's turn")
            coords = registerInput(player1) 
            current_turn = 2
        else:
            print("Player 2's turn")
            coords = registerInput(player2)
            current_turn = 1
            
        # 2. Check if someone won
        game_status = isGameOver(board, player1, player2)
    
    # 3. Game is over
    printBoard()
    displayResult(game_status) # Rodrigo's function