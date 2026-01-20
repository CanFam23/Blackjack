'''
NAME
    Card

DESCRIPTION
    This module provides a simple class for a playing card.
    It also provides unit testing for each of the class methods. 
             
Created by: Ted Wendt
Created on: February 1, 2022
Modified by: Nick Clouse
Modified on: January 19, 2026
'''

import tkinter as tk
from typing import Union

from PIL import ImageTk


class Card():
    '''
    A class used to represent a simple playing card.

    Attributes:
        __suit : str
            a string representing the suit of the card
        __face: str
            a string representing the 'face' of the card (e.g. 'J', 'A', '10', 'K'
        __value: int
            an integer used to compare cards against each other.  Typically numeric
            faces have the same value (i.e. a card with face '2' has value 2).  Other
            cards are defined by user. (e.g. 'J' has value 11)
        __image: Image
            a tkinter Image object used to render the card to a GUI

    Methods:
        Accessors:
            getSuit() : str
            getFace() : str
            getValue() : int
            getImage() : Image
        Dunders:
            __str__() : str
                returns a formatted string that includes the face and suit of the card
            __eq__(other: Card) : bool
            __ne__(other: Card) : bool
            __lt__(other: Card) : bool
            __le__(other: Card) : bool
            __gt__(other: Card) : bool
            __ge__(other: Card) : bool
        Other:
            draw(cvs: tkinter.Canvas, left: int, top: int) : None
                renders the card image to the specified canvas at coords (top, left).
    '''

    def __init__(self, face: str = None, suit: str = None, value: int = None, image: ImageTk.PhotoImage = None) -> None:  # type: ignore
        '''
        Constructor
        Parameters:
            face: str
            suit: str
            value: int
                the 'value' of the card (as defined by the game to be played).
                Typical ordering has A-2-3-4-5-6-7-8-9-10-J-Q-K.
                For alternate decks (e.g. UNO), ordering should be specified by user.
            image: tkinter Image
                the image of the card to be rendered to a GUI
        '''
        self.__suit = suit
        self.__face = face
        self.__value = value
        self.__image = image

    # ============================================
    # Accessor Methods
    # ============================================

    def getSuit(self) -> str:
        '''
            standard accessor method for __suit variable
            preconditions: None
            postconditions: returns suit
        '''
        return self.__suit

    def getFace(self) -> str:
        '''
            standard accessor method for __face variable
            preconditions: None
            postconditions: returns face
        '''
        return self.__face

    def getValue(self) -> int:
        '''
            standard accessor method for __value variable
            preconditions: None
            postconditions: returns value
        '''
        return self.__value

    def getImage(self):
        '''
            standard accessor method for __image variable

            preconditions: None
            postconditions: returns image
        '''
        return self.__image

    # ============================================
    # Other Methods
    # ============================================
    def draw(self, cvs: tk.Canvas, left: int, top: int) -> None:
        '''
            Draws the card image to the specified canvas.  Places the top left
            corner of the image at the coordinates (left, top).

            Parameters:

            preconditions: cvs must be a tkinter.Canvas object and must have already been instantiated
            postconditions: draws the card image to coordinates (left, top)
        '''
        cvs.create_image(left, top, image=self.__image, anchor="nw")

    def __str__(self) -> str:
        return f"{self.__face} of {self.__suit}"

    # ============================================
    # Comparison methods.
    # For the purposes of this course, we'll assume that all comparisons are done
    # based on the face value of the cards.
    # ============================================

    def __eq__(self, other) -> bool:
        return self.getValue() == other.getValue()

    def __lt__(self, other) -> bool:
        return self.getValue() < other.getValue()

    def __gt__(self, other) -> bool:
        return self.getValue() > other.getValue()

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __ge__(self, other) -> bool:
        return self > other or self == other

    def __ne__(self, other) -> bool:
        return not (self == other)

# End of class Card


# Begin unit testing
# NOTE: Image testing is not done in this module because of requirements from DeckOfCards class.
if __name__ == "__main__":
    # Test the default constructor
    print("Testing default constructor... ", end="")
    card1 = Card()
    assert card1.getFace() == None
    assert card1.getSuit() == None
    assert card1.getValue() == None
    assert card1.getImage() == None
    print("Passed!")

    print("Testing default constructor... ", end="")
    card2 = Card(face="A", value=1, suit="hearts")
    assert card2.getFace() == "A"
    assert card2.getSuit() == "hearts"
    assert card2.getValue() == 1
    assert card2.getImage() == None
    print("Passed!")

    print("Testing comparison methods...  ", end="")
    card3 = Card(face="2", value=2, suit="spades")
    card4 = Card(face="3", value=3, suit="clubs")
    card5 = Card(face="2", value=2, suit="hearts")
    assert card3 > card2
    assert card3 >= card2
    assert card3 >= card3
    assert card3 < card4
    assert card3 <= card4
    assert card4 <= card4
    assert card3 == card5
    assert card4 != card5
    print("Passed!")
