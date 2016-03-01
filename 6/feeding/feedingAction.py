from species import *
from playerState import *

class FeedingAction:

    # ARGUMENTS:
    # -- actionType should be one of "fat-tissue", "vegetarian", "attack", or False
    # -- callerSpecies is the player's species that will be fed according to the actionType given
    # -- tokens is a Nat of food tokens fat tissue should store
    # -- defender is a PlayerState who owns the prey to be attacked
    # -- prey is the species (owned by defender) that the caller wishes to attack
    # these arguments are REALLY OPTIONAL -- if you don't give enough information, an exception will be called
    # if you give TOO MUCH information (ex: FeedingAction("vegetarian", Species, 3, 0))
    # then the actionType passed in will be followed and other information will be ignored
    # it will output a tuple describing the action
    # String, (Opt:Species), (Opt: Nat), (Opt: PlayerState), (Opt: Species)
    #               -> One of False, List(String, at least one (Opt: Species), Opt(Nat), Opt(PlayerState), Opt(Species))
    @staticmethod
    def createAction(actionType, callerSpecies=None, tokens=0, defender=None, prey=None):
        # no more feeding turns
        if not actionType:
            return False
        if callerSpecies:
            if actionType == "fat-tissue" and tokens:
                return [callerSpecies, tokens]
            if actionType == "vegetarian":
                return [callerSpecies]
            if actionType == "attack" and defender and prey:
                return [callerSpecies, defender, prey]

    # Create a json representation of the given action to send out to a remote
    # FeedingAction -> array of Json
    @staticmethod
    def toJsonArray(action):
        if not action:
            return False

        # vegetarian
        if len(action) == 1:
            return action[0].toJsonArray()
        # fat tissue
        if len(action) == 2:
            return [action[0].toJsonArray(), action[1]]
        # attack
        if len(action) == 3:
            return [action[0].toJsonArray(), action[1].toJsonArray(), action[2].toJsonArray()]

    # Create an object from a json array
    # array of Json -> FeedingAction
    @staticmethod
    def jsonToFeeding(input):
        if not input:
            return False
        if (len(input) == 4 or len(input) == 5) and Species.convertSpecies(input):
            return [Species.convertSpecies(input)]
        if len(input) == 2:
            return [Species.convertSpecies(input[0]), int(input[1])]
        if len(input) == 3:
            return [Species.convertSpecies(input[0]), PlayerState.convertPlayerState(input[1]),
                                                                                    Species.convertSpecies(input[2])]