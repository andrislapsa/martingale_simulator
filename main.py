import sys, getopt
from termcolor import colored, cprint
import roulette
import player

# default arguments

def getArguments() :
	roundsToPlay = 10
	startingBalance = 1000
	startingBet = 1
	simulations = 1
	showDetailedInfo = False

	argv = sys.argv[1:]
	opts, args = getopt.getopt(argv, "", [
		"rounds=",
		"startingBalance=",
		"startingBet=",
		"simulations=",
		"showDetailedInfo="
	])

	for opt, arg in opts :
		if opt == "--rounds" :
			roundsToPlay = int(arg)
		elif opt == "--startingBalance" :
			startingBalance = int(arg)
		elif opt == "--startingBet" :
			startingBet = int(arg)
		elif opt == "--simulations" :
			simulations = int(arg)
		elif opt == "--showDetailedInfo" :
			showDetailedInfo = True if arg == "1" else False

	return {
		"roundsToPlay": roundsToPlay,
		"startingBalance": startingBalance,
		"startingBet": startingBet,
		"simulations": simulations,
		"showDetailedInfo": showDetailedInfo
	}

arguments = getArguments()

successfulGames = 0
totalProfit = 0
averageProfit = 0

print "Will run %s simulations, each game will attempt to play %d rounds with starting balance of %d and starting bet as %d" % (
	arguments["simulations"], arguments["roundsToPlay"], arguments["startingBalance"], arguments["startingBet"]
)

def printFormattedRoundResult(gameInfo) :
	gameResult = gameInfo["gameResult"]

	eurSign = u"\u20AC"
	colorMap = { "black": "grey", "red": "red", "green": "green" }
	status = colored(
		(gameResult["status"] + "!").upper(),
		("green" if gameResult["status"] == "won" else "red"), attrs=["bold"]
	)

	cprint(
		"=== game #%d ===" % gameInfo["gameNumber"],
		"grey", attrs=["bold"]
	)

	print "Balance: %d%s - %d%s = %d%s" % (
		gameInfo["balanceBeforeBet"], eurSign,
		gameResult["placedBet"]["amount"], eurSign,
		gameInfo["balanceAfterBet"], eurSign
	)

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

for simulation in range(arguments["simulations"]) :
	game = roulette.Roulette()
	gambler = player.Player(arguments["startingBalance"], arguments["startingBet"])
	gameProfit = 0

	gameInfo = {}

	for gameNumber in range(arguments["roundsToPlay"]) :
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

		if arguments["showDetailedInfo"] :
			print "heeei"
			printFormattedRoundResult(gameInfo)

	cprint(
		"=== simulation #%d ===" % (simulation + 1),
		"grey", attrs=["bold"]
	)

	successfulGame = gameInfo["balanceAfterSpin"] > arguments["startingBalance"]

	status = colored(
		"[%s]" % ("success" if successfulGame else "fail"),
		("green" if successfulGame else "red"), attrs=["bold"]
	)

	if successfulGame :
		successfulGames += 1

	gameProfit = gameInfo["balanceAfterSpin"] - arguments["startingBalance"]
	totalProfit += gameProfit

	print "%s rounds played: %d final balance %d total profit %d" % (status, gameInfo["gameNumber"], gameInfo["balanceAfterSpin"], gameProfit)

successfulGameRate = float(successfulGames) / float(arguments["simulations"]) * 100
averageProfit = float(totalProfit) / float(arguments["simulations"])

print "=== summary ==="
print "Total successful games: %d (rate %f%%) average profit %d" % (successfulGames, successfulGameRate, averageProfit)





