from Tkinter import *
from traitCard import TraitCard
from species import *
from playerState import PlayerState
from dealer import Dealer

class Drawing:

	"""
		Only pass in dealer OR player -- not both
	"""
	def __init__(self, root, dealer=None, player=None):	
		self.exTrait = TraitCard("carnivore", 5)
		self.exTrait2 = TraitCard("fat-tissue", 3)
		self.exTrait3 = TraitCard("long-neck", 1)
		self.exTrait4 = TraitCard("scavenging", 3)
		self.exTrait5 = TraitCard("climbing", 3)
		self.exSpecies = Species(2, 3, 4, [], 0)
		self.exSpecies2 = Species(1, 2, 3, ["fat-tissue", "carnivore"], 1)
		self.exSpecies3 = Species(0, 1, 2, ["long-neck", "cooperation", "scavenging"], 0)
		self.exPlayer = PlayerState(1, 3, [self.exSpecies], [self.exTrait])
		self.exPlayer2 = PlayerState(2, 5, [self.exSpecies2, self.exSpecies3], [self.exTrait2, self.exTrait3])
		self.exDealer= Dealer([self.exPlayer, self.exPlayer2], 10, [self.exTrait, self.exTrait2, self.exTrait3, self.exTrait4, self.exTrait5])
		player = self.exPlayer
		dealer = self.exDealer

		if dealer is not None:
			dealerMaster = self.drawDealer(root, dealer)
			dealerMaster.grid(row=0, column=0)
		if player is not None:
			playerMaster = self.drawPlayer(root, player)
			playerMaster.grid(row=0, column=0)
		if dealer is None and player is None:
			raise ValueError("Must give a dealer or a player")


	def drawDealer(self, master, dealer, row=0, column=0):
		dealerFrame = LabelFrame(master, text="Dealer", padx=10, pady=10)
		dealerFrame.grid(row=row, column=column)

		playersFrame = LabelFrame(dealerFrame, text="Players", padx=10, pady=10)
		"""
		# bind a vertical scrollbar to the list of players
		vertscroll = Scrollbar(playersFrame, orient="vertical")
		vertscroll.grid(row=row, column=column+2, sticky="NS", rowspan=len(dealer.players))
		canv = Canvas(playersFrame, yscrollcommand=vertscroll.set, scrollregion=(0, 0, 800, 800))
		canv.grid(row=row, column=column, sticky="NEWS")
		vertscroll.config(command=canv.yview)
		"""
		playersFrame.grid(row=row, column=column)

		for i in range(len(dealer.players)):
			self.drawPlayer(playersFrame, dealer.players[i], row=row+i, column=column)

		self.makeLabelFrame(dealerFrame, "Watering Hole", dealer.wateringHole, row=row, column=column+1)

		deckText = str(len(dealer.deck)) + " cards left"
		self.makeLabelFrame(dealerFrame, "Deck", deckText, row=row+1, column=column+1)

		return dealerFrame


	def drawPlayer(self, master, player, row=0, column=0):
		ptext = "Player " + str(player.num)
		playerFrame = LabelFrame(master, text=ptext, padx=10, pady=10)
		# bind a horizontal scrollbar to this player
		"""
		horiscroll = Scrollbar(playerFrame, orient="horizontal")
		horiscroll.grid(row=row+2, column=column, sticky="WE", columnspan=len(player.species)+1)
		canv = Canvas(playerFrame, xscrollcommand=horiscroll.set, scrollregion=(0, 0, 500, 300))
		canv.grid(row=row, column=column, sticky="NEWS")
		horiscroll.config(command=canv.xview)
		"""
		playerFrame.grid(row=row, column=column)


		self.makeLabelFrame(playerFrame, "Food Bag", player.foodbag, row=row, column=column)
		
		speciesFrame = LabelFrame(playerFrame, text="Species List", padx=10, pady=10)
		speciesFrame.grid(row=row, column=column+1)

		for i in range(len(player.species)):
			self.drawSpecies(speciesFrame, player.species[i], row=row, column=column+i+2)
		
		row += 1

		handFrame = LabelFrame(playerFrame, text="Hand", padx=10, pady=10)
		handFrame.grid(row=row, column=column)

		for i in range(len(player.hand)):
			self.drawTraitCard(handFrame, player.hand[i], row=row, column=column+i)
		
		return playerFrame

	def drawSpecies(self, master, species, row=0, column=0):
		speciesFrame = LabelFrame(master, text="Species", padx=10, pady=10)
		speciesFrame.grid(row=row, column=column)

		for i in range(len(species.traits)):
			self.makeLabelFrame(speciesFrame, "Trait", species.traits[i], row=row, column=column+i)

		row += 1

		foodFrame = self.drawFood(speciesFrame, species.food)
		foodFrame.grid(row=row, column=column)

		self.makeLabelFrame(speciesFrame, "Body", species.body, row=row, column=column+1)
		self.makeLabelFrame(speciesFrame, "Population", species.population, row=row, column=column+2)

		if species.hasTrait("fat-tissue") and species.fatFood > 0:
			self.makeLabelFrame(speciesFrame, "Fat Food", species.fatFood, row=row, column=column+3)


		return speciesFrame

	def drawFood(self, master, food, row=0, column=0):
		foodFrame = LabelFrame(master, text="Food", padx=10, pady=10)
		foodFrame.grid(row=row, column=column)

		photo = PhotoImage(file="ham.gif")
		ham = Label(master=foodFrame, image=photo)
		ham.image = photo
		ham.grid(row=row, column=column)

		xNum = "x" + str(food)
		xNumLabel = Label(master=foodFrame, text=xNum)
		xNumLabel.grid(row=row+1, column=column)

		return foodFrame

	def drawTraitCard(self, master, card, row=0, column=0):
		label = card.name + ", " + str(card.food) 
		self.makeLabelFrame(master, "Trait", label, row, column)

	def makeLabelFrame(self, master, titleText, bodyText, row=0, column=0):
		titleFrame = LabelFrame(master=master, text=titleText, padx=10, pady=10)
		titleFrame.grid(row=row, column=column, sticky="NEWS")
		bodyLabel = Label(master=titleFrame, text=str(bodyText))
		bodyLabel.grid(row=row+1, column=column)


root = Tk()
drawing = Drawing(root)
root.mainloop()