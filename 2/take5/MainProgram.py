import sys
sys.path.append('../../3/take5')
from Dealer import *
from Player import *
import Constants


class MainProgram:
    @staticmethod
    # Processes the command line number of players and kicks off the game
    # if a strategy is to be assigned to a player, it assigns it
    # prints out a string containing the leaderboard once the game has finished
    # runProgram: Nat -> String
    def runProgram(numPlayers):
        players = []

        if numPlayers * Constants.CARDS_PER_PLAYER + Constants.NUM_STACKS > Constants.MAX_FACE_VALUE:
            print "Too many players, not enough cards"
            quit()
        if numPlayers < 2:
            print "Too few players"
            quit()

        for i in range(numPlayers):
            players.append(Player(i))
        dealer = Dealer(players)
        return dealer.playGame()

if __name__ == "__main__":
    MainProgram.runProgram(int(sys.argv[1]))
