'''
file: BlackjackPlayer.py 

description: This file contains a simple class for a blackjack player, 
which stores the players name, hand, and total value and includes methods
for adding cards, updating hand value, checking for a bust, and getting the hand / value
'''

from Card import Card

class BlackjackPlayer(object):
    def __init__(self, name = 'player'):
        """
        Creates a new BlackjackPlayer object
        
        :param name: Name of player, defaults to 'player'
        """
        self.name = name
        self.__hand = []
        self.__totalValue = 0
        
    def addCard(self, c: Card) -> None:
        """
        Add card to players hand
        
        :param c: Card to add to hand
        :type c: Card
        """
        self.__hand.append(c)
        
    def addToValue(self, num: int) -> None:
        """
        Adds the given number to the players total hand value
        
        :param num: Number to add
        :type num: int
        """
        self.__totalValue += num
        
    def getTotalValue(self) -> int:
        """
        Get users current total value of their hand
        :return: The total value of the players hand
        :rtype: int
        """
        return self.__totalValue
    
    def bust(self) -> bool:
        """
        Returns true if the players hand is over 21, false otherwise.
        :return: If the player has busted
        :rtype: bool
        """
        return self.__totalValue > 21
    
    def getHand(self) -> list[Card]:
        """        
        Returns the users hand
        :return: The players hand
        :rtype: list[Card]
        """
        return self.__hand