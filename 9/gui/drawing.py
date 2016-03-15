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
		self.exSpecies = Species(2, 3, 4, ["fat-tissue", "foraging"], 0)
		self.exPlayer = PlayerState(1, 3, [self.exSpecies], [self.exTrait])
		#self.exDealer= Dealer([self.exPlayer], 10, [self.exTrait, self.exTrait])
		player = self.exPlayer
		if dealer is not None:
			master = self.drawDealer(root, dealer)
			master.pack()
		elif player is not None:
			master = self.drawPlayer(root, player)
			master.pack()
		else:
			raise ValueError("Must give a dealer XOR a player")


	def drawPlayer(self, master, player):
		ptext = "Player " + str(player.num)
		playerFrame = LabelFrame(master, text=ptext, padx=10, pady=10)
		playerFrame.pack()

		self.makeLabelFrame(playerFrame, "Food Bag", player.foodbag)

		for species in player.species:
			self.drawSpecies(playerFrame, species)

		handFrame = LabelFrame(playerFrame, text="Hand", padx=10, pady=10)
		handFrame.pack()

		for card in player.hand:
			self.drawTraitCard(handFrame, card)

		return playerFrame

	def drawSpecies(self, master, species):
		speciesFrame = LabelFrame(master, text="Species", padx=10, pady=10)
		speciesFrame.pack()

		foodFrame = self.drawFood(speciesFrame, species.food)
		foodFrame.pack()

		self.makeLabelFrame(speciesFrame, "Body", species.body)
		self.makeLabelFrame(speciesFrame, "Population", species.population)

		if species.hasTrait("fat-tissue") and species.fatFood > 0:
			self.makeLabelFrame(speciesFrame, "Fat Food", species.fatFood)

		for trait in species.traits:
			self.makeLabelFrame(speciesFrame, "Trait", trait)

		return speciesFrame

	def drawFood(self, master, food):
		foodFrame = LabelFrame(master, text="Food", padx=10, pady=10)
		foodFrame.pack()

		photo = PhotoImage(file="ham.gif")
		ham = Label(master=foodFrame, image=photo)
		ham.image = photo
		ham.pack()

		xNum = "x" + str(food)
		xNumLabel = Label(master=foodFrame, text=xNum)
		xNumLabel.pack()

		return foodFrame

	def drawTraitCard(self, master, card):
		label = card.name + ", " + str(card.food) 
		self.makeLabelFrame(master, "Trait", label)

	def makeLabelFrame(self, master, titleText, bodyText):
		titleFrame = LabelFrame(master=master, text=titleText, padx=10, pady=10)
		titleFrame.pack()
		bodyLabel = Label(master=titleFrame, text=str(bodyText))
		bodyLabel.pack()


root = Tk()
drawing = Drawing(root)
root.mainloop()