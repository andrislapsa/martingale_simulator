import random

# Class for roulette result simulation
class Roulette :
	betSpots = {}

	placedBet = {
		"amount": "",
		"color": 0
	}

	def __init__(self) :
		self.createBetspots()
	
	def createBetspots(self) :
		total = 37

		for i in range(total) :
			color = "red"

			if i == 0 :
				color = "green"

			if i > total / 2 :
				color = "black"

			self.betSpots[i] = color;

	def placeBet(self, color, amount) :
		self.placedBet = {
			"color": color,
			"amount": amount
		}

	def spin(self) :
		return random.choice(self.betSpots.keys())

	def getColor(self, number) :
		return self.betSpots[number]

	def getResult(self) :
		resultNumber = self.spin()
		resultColor = self.getColor(resultNumber)
		status = "lost"

		if resultColor == self.placedBet["color"] :
			status = "won"

		return {
			"result": resultColor,
			"status": status,
			"placedBet": self.placedBet
		}