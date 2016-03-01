#!/usr/bin/env python

# Austin Colcord and Sam Lucyk
# This program is the implementation of the player interface

from abc import abstractmethod


class Player(object):
    """
    This is the class for Player, which contains a player number (id), strategy,
    bull_point count, and a list of cards
    """

    def __init__(self, player_num, strategy=None):
        """
        This is the init function that sets the player_num, strategy, bull points, and cards

        :param player_num: Nat - the player's ID number
        :param strategy: Nat - the strategy number
        :return: Player
        """
        self.player_num = player_num
        self.strategy = 0
        self.bullPoints = 0
        self.cards = []

    @abstractmethod
    def choose_card(self):
        """
        Places a card in hand on board based on the strategy of the player

        :return: Card - the max card in this player's list
        """
        pass

    def add_bull_points(self, n):
        """
        Adds the given number to the player's bull points

        :param n: Nat - number of bull points
        :return: Void
        """
        self.bullPoints = self.bullPoints + n
