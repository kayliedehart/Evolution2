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
			master.grid(row=0, column=0)
		elif player is not None:
			master = self.drawPlayer(root, player)
			master.grid(row=0, column=0)
		else:
			raise ValueError("Must give a dealer XOR a player")


	def drawPlayer(self, master, player, row=0, column=0):
		ptext = "Player " + str(player.num)
		playerFrame = LabelFrame(master, text=ptext, padx=10, pady=10)
		playerFrame.grid(row=row, column=column)

		foodBagFrame = LabelFrame(playerFrame, text="Food Bag", padx=10, pady=10)
		foodBagFrame.grid(row=row, column=column)
		foodBagLabel = Label(master=foodBagFrame, text=str(player.foodbag))
		foodBagLabel.grid(row=row, column=column)
		
		speciesFrame = LabelFrame(playerFrame, text="Species", padx=10, pady=10)
		speciesFrame.grid(row=row, column=column+1)

		for i in range(len(player.species)):
			self.drawSpecies(speciesFrame, player.species[i], row=row, column=column+i+2)
		
		handFrame = LabelFrame(playerFrame, text="Hand", padx=10, pady=10)
		handFrame.grid(row=row+1, column=column)

		for i in range(len(player.hand)):
			self.drawTraitCard(handFrame, player.hand[i], row=row+1, column=column+i)
		
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
		titleFrame.grid(row=row, column=column)
		bodyLabel = Label(master=titleFrame, text=str(bodyText))
		bodyLabel.grid(row=row+1, column=column)


root = Tk()
drawing = Drawing(root)
root.mainloop()