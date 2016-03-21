from Tkinter import *
import os
CUR_PATH = os.path.dirname(os.path.abspath(__file__))

class Drawing:

	"""
		Only pass in dealer OR player -- not both
		or don't
		i'm a comment, not a cop
	"""
	def __init__(self, dealer=None, player=None):	
		root = Tk()
		self.canvas = Canvas(root, width=800, height=600)
		self.dealerMaster = self.playerMaster = None

		if dealer is not None:
			self.dealerMaster = self.drawDealer(self.canvas, dealer)
			self.dealerMaster.grid(row=0, column=0)
			self.createScrollbars(root, self.dealerMaster)
		elif player is not None:
			self.playerMaster = self.drawPlayer(self.canvas, player)
			self.playerMaster.grid(row=0, column=0)
			self.createScrollbars(root, self.playerMaster)
		if dealer is None and player is None:
			raise ValueError("Must give a dealer or a player")

		root.mainloop()
		root.destroy

	"""
		Create scrollbars for the window
		LabelFrame or None, LabelFrame or None -> Void
	"""
	def createScrollbars(self, root, master):
		vertiscroll = Scrollbar(root, orient="vertical", command=self.canvas.yview)
		horizscroll = Scrollbar(root, orient="horizontal", command=self.canvas.xview)
		self.canvas.configure(yscrollcommand=vertiscroll.set, xscrollcommand=horizscroll.set)
		vertiscroll.pack(side="right", fill="y")
		horizscroll.pack(side="bottom", fill="x")
		self.canvas.pack(fill="both", expand="yes")
		self.canvas.create_window((0, 0,), window=master, anchor="nw")
		master.bind("<Configure>", self.rootFrameConfigure)

	"""
		Event handler to move the canvas when a scrollbar is moved
		Event -> Void
	"""
	def rootFrameConfigure(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))		

	"""
		Create a LabelFrame containing representations of everything within the Dealer
		Tk, Dealer, Opt: Nat, Opt:Nat -> LabelFrame
	"""
	def drawDealer(self, master, dealer, row=0, column=0):
		dealerFrame = LabelFrame(master, text="Dealer", padx=10, pady=10)
		dealerFrame.grid(row=row, column=column)

		self.makeLabelFrame(dealerFrame, "Watering Hole", "{} tokens".format(dealer.wateringHole), row=row, column=column)
		self.makeLabelFrame(dealerFrame, "Deck", "{} cards left".format(len(dealer.deck)), row=row+1, column=column)

		column += 1

		playersFrame = LabelFrame(dealerFrame, text="Players", padx=10, pady=10)
		playersFrame.grid(row=row, column=column, rowspan=len(dealer.players))
		for i in range(len(dealer.players)):
			self.drawPlayer(playersFrame, dealer.players[i], row=row+i, column=column)

		return dealerFrame

	"""
		Create a LabelFrame containing representations of everything within the Player
		Tk, Player, Opt: Nat, Opt:Nat -> LabelFrame
	"""
	def drawPlayer(self, master, player, row=0, column=0):
		ptext = "Player " + str(player.num)
		playerFrame = LabelFrame(master, text=ptext, padx=10, pady=10)
		playerFrame.grid(row=row, column=column, sticky="nw")

		self.makeLabelFrame(playerFrame, "Food Bag", "{} tokens".format(player.foodbag), row=row, column=column)
		
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

	"""
		Create a LabelFrame containing representations of everything within the Species
		Tk, Species, Opt: Nat, Opt:Nat -> LabelFrame
	"""
	def drawSpecies(self, master, species, row=0, column=0):
		speciesFrame = LabelFrame(master, text="Species", padx=10, pady=10)
		speciesFrame.grid(row=row, column=column)

		for i in range(len(species.traits)):
			self.makeLabelFrame(speciesFrame, "Trait", species.traits[i], row=row, column=column+i)

		row += 1

		foodFrame = self.drawFood(speciesFrame, species.food)
		foodFrame.grid(row=row, column=column)

		column += 1
		self.makeLabelFrame(speciesFrame, "Body", species.body, row=row, column=column)
		column += 1
		self.makeLabelFrame(speciesFrame, "Population", species.population, row=row, column=column)
		column += 1
		if species.hasTrait("fat-tissue") and species.fatFood > 0:
			self.makeLabelFrame(speciesFrame, "Fat Food", species.fatFood, row=row, column=column)

		return speciesFrame


	"""
		Draw the food a Species has with an illustration
		Tk, Nat, Opt: Nat, Opt: Nat -> LabelFrame
	"""
	def drawFood(self, master, food, row=0, column=0):
		foodFrame = LabelFrame(master, text="Food", padx=10, pady=10)
		foodFrame.grid(row=row, column=column)

		photo = PhotoImage(file=CUR_PATH+"/ham.gif")
		ham = Label(master=foodFrame, image=photo)
		ham.image = photo # save a reference
		ham.grid(row=row, column=column)

		xNum = "x" + str(food)
		xNumLabel = Label(master=foodFrame, text=xNum)
		xNumLabel.grid(row=row+1, column=column)

		return foodFrame

	"""
		Create a LabelFrame containing TraitCard
		Tk, TraitCard, Opt: Nat, Opt:Nat -> LabelFrame
	"""
	def drawTraitCard(self, master, card, row=0, column=0):
		self.makeLabelFrame(master, "Trait", "{}, {}".format(card.name, card.food), row, column)

	"""
		Create a LabelFrame with a title, then draw a label with contents inside that LabelFrame
		Tk, String, String, Opt: Nat, Opt:Nat -> LabelFrame
	"""
	def makeLabelFrame(self, master, titleText, bodyText, row=0, column=0):
		titleFrame = LabelFrame(master=master, text=titleText, padx=10, pady=10)
		titleFrame.grid(row=row, column=column, sticky="NEWS")
		bodyLabel = Label(master=titleFrame, text=str(bodyText))
		bodyLabel.grid(row=row+1, column=column)

if __name__ == "__main__":
	Drawing()

