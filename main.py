import sys
from termcolor import colored, cprint
import roulette
import player

if sys.argv[1] == "help" :
	print "arguments: gamesToPlay balance startingBet"
	exit()

gamesToPlay = int(sys.argv[1]) if sys.argv[1] else 10
balance = int(sys.argv[2]) if sys.argv[2] else 1000
startingBet = int(sys.argv[3]) if sys.argv[3] else 1

print "Will attempt to play %d games with balance of %d and using starting bet as %d" % (
	gamesToPlay, balance, startingBet
)

game = roulette.Roulette()
gambler = player.Player(balance, startingBet)

def printFormattedRoundResult(gameResult, gambler) :
	eurSign = u"\u20AC"
	colorMap = { "black": "grey", "red": "red", "green": "green" }
	balance = colored(str(gambler.balance) + eurSign, ("green" if gameResult["status"] == "won" else "red"), attrs=["bold"])

	print "[balance: %s] Gambler placed %s%s on %s, ball landed on %s" % (
		balance,
		colored(gambler.betAmount, "grey", attrs=["bold"]),
		eurSign,
		colored(gambler.betColor, colorMap[gambler.betColor], attrs=["bold"]),
		colored(gameResult["result"], colorMap[gameResult["result"]], attrs=["bold"]),
	)

for gameNumber in range(gamesToPlay) :
	game.placeBet(gambler.betColor, gambler.betAmount)

	gameResult = game.getResult()

	printFormattedRoundResult(gameResult, gambler)

	won = gameResult["status"] == "won"

	if won :
		gambler.resetBet()
		gambler.changeColor()
	else :
		gambler.doubleBet()

	gambler.updateBalance(won)