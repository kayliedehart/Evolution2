class Card:

    # Instantiates card with a face value and bullpoints
    # __init__: Nat, Nat -> Card
    def __init__(self, faceValue, bullPoints):
        self.faceValue = faceValue
        self.bullPoints = bullPoints

    # Override str to make readable Card printouts
    def __str__(self):
        return "Face Value: " + str(self.faceValue) + " Bull Points: " + str(self.bullPoints)

    # Override eq to make cards with same values equal
    def __eq__(self, other):
        if isinstance(other, Card):
            return self.faceValue == other.faceValue and self.bullPoints == other.bullPoints
        return False
