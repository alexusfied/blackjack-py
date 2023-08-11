from game import Game

if (__name__ == "__main__"):
    # Creaet an instance of the Game class
    currentGame = Game()
    # The outer loop keeps the overall game running until the player quits or has lost all of his money
    while True:
        currentGame.prepNewRound()
        print("-------------------------------")
        print("The game is on!\n")
        currentGame.dealFirst()
        # The inner loop keeps each round running until the player or dealer has won or there is a tie
        while currentGame.gameOn:
            currentGame.gameOn = currentGame.takeTurn()
        # After each round the player gets to decide whether the game should keep running
        if currentGame.play_again():
            continue
        else:
            break