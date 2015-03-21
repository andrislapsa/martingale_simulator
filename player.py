# Player class manages strategical betting
# decisions and manipulates available funds
class Player :

	# remaining balance for player
	balance = 0

	# color that player wants to bet on
	betColor = "black"

	# how much will player bet
	betAmount = 0

	# defines starting bet
	startingBet = 0

	def __init__(self, balance, startingBet) :
		self.balance = balance
		self.startingBet = startingBet
		self.resetBet()

	def changeColor(self) :
		if self.betColor == "black" :
			self.betColor = "red"
		else :
			self.betColor = "black"

	def doubleBet(self) :
		self.betAmount *= 2

	def resetBet(self) :
		self.betAmount = self.startingBet

	def placeBet(self) :
		if self.betAmount > self.balance :
			return False

		self.balance -= self.betAmount
		return True

	def receiveWinnings(self) :
		amountWon = self.betAmount * 2
		self.balance += amountWon
		return amountWon
