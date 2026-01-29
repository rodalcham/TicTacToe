board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]

player1 = {'turn': -1, 'symbol': ''}
player2 = {'turn': -1, 'symbol': ''}

import random

def genRandom(lowB, upB):
    return random.randrange(lowB, upB)

def displayResult(res):
    if res == 0:
        print("Game continues...") #For testing
    elif res == 1:
        print("Game Over: Player 1 wins!")
    elif res == 2:
        print("Game Over: Player 2 wins!")
    elif res == 3:
        print("Game Over: It's a draw!")
        
def main():
    print("Testing genRandom function:")
    print("-" * 30)
    for i in range(5):
        rand_num = genRandom(1, 10)
        print(f"Random number {i+1}: {rand_num}")
    
    print("\n" + "=" * 30)
    print("Testing displayResult function:")
    print("-" * 30)
    
    for result in range(4):
        print(f"\nResult code {result}:")
        displayResult(result)
    
    print("\n" + "=" * 30)
    print("Combined test - Random results:")
    print("-" * 30)
    
    for i in range(5):
        random_result = genRandom(0, 4)  # Generates 0, 1, 2, or 3
        print(f"\nTest {i+1} - Random result: {random_result}")
        displayResult(random_result)

if __name__ == "__main__":
    main()

