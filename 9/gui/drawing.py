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
		self.exSpecies = Species(2, 3, 4, [self.exTrait, self.exTrait2], 0)
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

		foodBagFrame = LabelFrame(playerFrame, text="Food Bag", padx=3, pady=3)
		foodBagFrame.pack()
		foodBagLabel = Label(foodBagFrame, text=str(player.foodbag))
		foodBagLabel.pack()

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

		bodyFrame = LabelFrame(speciesFrame, text="Body")
		bodyFrame.pack()
		bodyLabel = Label(master=bodyFrame, text=species.body)

		popFrame = LabelFrame(speciesFrame, text="Population")
		popFrame.pack()
		popLabel = Label(master=popFrame, text=species.population)

		if species.hasTrait("fat-tissue"):
			fatFoodFrame = LabelFrame(speciesFrame, text="Fat Food")
			fatFoodFrame.pack()
			fatFoodLabel = Label(master=fatFoodFrame, text=species.fatFood)

		for card in species.traits:
			self.drawTraitCard(speciesFrame, card)


	def drawFood(self, master, food):
		foodFrame = LabelFrame(master, text="FOOD", padx=10, pady=10)
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
		traitFrame = LabelFrame(master, text="TRAIT", padx=10, pady=10)
		traitFrame.pack()

		label = card.name + ", " + str(card.food) 
		labelTrait = Label(master=traitFrame, text=label)
		labelTrait.pack()




root = Tk()

drawing = Drawing(root)

root.mainloop()