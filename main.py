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

simulations = 1
successfulGames = 0

print "Will attempt to play %d games with balance of %d and using starting bet as %d" % (
	gamesToPlay, balance, startingBet
)

def printFormattedRoundResult(gameInfo) :
	gameResult = gameInfo["gameResult"]

	eurSign = u"\u20AC"
	colorMap = { "black": "grey", "red": "red", "green": "green" }
	status = colored(
		(gameResult["status"] + "!").upper(),
		("green" if gameResult["status"] == "won" else "red"), attrs=["bold"]
	)

	# print "%d, %d" % (gameResult["placedBet"]["amount"], gameInfo["balanceAfterBet"])

	cprint(
		"=== game #%d ===" % gameInfo["gameNumber"],
		"grey", attrs=["bold"]
	)

	print "Balance: %d%s - %d%s = %d%s" % (
		gameInfo["balanceBeforeBet"], eurSign,
		gameResult["placedBet"]["amount"], eurSign,
		gameInfo["balanceAfterBet"], eurSign
	)

	# print gameInfo
	print "Gambler placed %s%s on %s, ball landed on %s and in result %s" % (
		gameResult["placedBet"]["amount"], eurSign,
		colored(gameResult["placedBet"]["color"], colorMap[gameResult["placedBet"]["color"]], attrs=["bold"]),
		colored(gameResult["result"], colorMap[gameResult["result"]], attrs=["bold"]),
		status,
	)

	print "Balance: %d%s + %d%s = %d%s" % (
		gameInfo["balanceAfterBet"], eurSign,
		gameInfo["amountWon"], eurSign,
		gameInfo["balanceAfterSpin"], eurSign
	)

for simulation in range(simulations) :
	game = roulette.Roulette()
	gambler = player.Player(balance, startingBet)

	gameInfo = {}

	for gameNumber in range(gamesToPlay) :
		gameInfo = {
			"gameNumber": gameNumber + 1,
			"balanceBeforeBet": gambler.balance
		}

		game.placeBet(gambler.betColor, gambler.betAmount)
		if not gambler.placeBet() :
			gameInfo["balanceAfterSpin"] = gambler.balance
			# print "GAME OVER!"
			break

		gameInfo["balanceAfterBet"] = gambler.balance

		gameResult = game.getResult()
		gameInfo["gameResult"] = gameResult

		won = gameResult["status"] == "won"
		amountWon = 0

		if won :
			amountWon = gambler.receiveWinnings()
			gambler.resetBet()
			gambler.changeColor()
		else :
			gambler.doubleBet()

		gameInfo["amountWon"] = amountWon
		gameInfo["balanceAfterSpin"] = gambler.balance

		printFormattedRoundResult(gameInfo)

	# cprint(
	# 	"=== simulation #%d ===" % (simulation + 1),
	# 	"grey", attrs=["bold"]
	# )

	# print gameInfo

	if gameInfo["balanceAfterSpin"] > balance :
		successfulGames += 1

	# print "Games played: %d final balance %d" % (gameInfo["gameNumber"], gameInfo["balanceAfterSpin"])

print "Total successful games: %d" % successfulGames





