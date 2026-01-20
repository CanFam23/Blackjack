'''
file: BlackjackGame.py 

description: This file contains the BlackjackGame class, which handles the game logic and rendering for a 
Blackjack game on a TKinter window.
'''
import tkinter as tk

from blackjack.BlackjackPlayer import BlackjackPlayer as BP
from blackjack.DeckOfCards import DeckOfCards as DC

DELAY_SEC = 1500

BG_COLOR = 'green'

TEXT_COLOR_DEFAULT = 'white'
TEXT_COLOR_GOOD = 'green'
TEXT_COLOR_BAD = 'red'

WINDOW_HEIGHT = 439
WINDOW_WIDTH = 510

class BlackjackGame(object):
    def __init__(self, wn: tk.Tk):
        """
        Initializes a new BlackjackGame object

        :param wn: TKinter window to display game on.
        :type wn: tk.Tk
        """
        wn.title('Blackjack')
        wn.resizable(width=False, height=False)

        # Get screen dimensions
        screen_width = wn.winfo_screenwidth()
        screen_height = wn.winfo_screenheight()

        # Calculate position to center
        x = (screen_width - WINDOW_WIDTH) // 2
        y = (screen_height - WINDOW_HEIGHT) // 2

        wn.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

        # Configure grid weights to center content
        wn.grid_rowconfigure(0, weight=1)
        wn.grid_rowconfigure(1, weight=1)
        wn.grid_rowconfigure(2, weight=1)
        wn.grid_rowconfigure(3, weight=1)
        wn.grid_columnconfigure(0, weight=1)
        wn.grid_columnconfigure(1, weight=1)

        self.__instructionsFrame = tk.LabelFrame(wn, text="Welcome to Blackjack", width=100, height=100)
        self.__instructionsFrame.grid(row=0, column=0, columnspan=2, padx=0, pady=0)

        self.__instructionsText = tk.Label(self.__instructionsFrame, font=("Arial", 14),
                                        text="House Rules:\n1. Aces are always low. \n2. No splitting (But you can try)\n3. Dealer stands on 17")
        self.__instructionsText.pack()

        # Create deck and player / dealer
        self.__blackjackDeck = DC('deck_of_cards.png')
        self.__player = BP('Player')
        self.__dealer = BP('Dealer')

        # Keeps track of if its dealers turn, helpful for rendering
        self.__dealerTurn = False

        self.__gameOver = False

        # Need to be declared in here to ensure DC width and height are set
        FRAME_WIDTH = 52*3 + DC.width
        FRAME_HEIGHT = DC.height * 1.5

        # Set up the canvases
        self.__playerFrame = tk.LabelFrame(
            wn, text="Player", width=FRAME_WIDTH, height=FRAME_HEIGHT, bg=BG_COLOR)
        self.__pCanvas = tk.Canvas(
            self.__playerFrame, width=FRAME_WIDTH, height=FRAME_HEIGHT, bg=BG_COLOR)
        self.__dealerFrame = tk.LabelFrame(
            wn, text="Dealer", width=FRAME_WIDTH, height=FRAME_HEIGHT, bg=BG_COLOR)
        self.__dealerCanvas = tk.Canvas(
            self.__dealerFrame, width=FRAME_WIDTH, height=FRAME_HEIGHT, bg=BG_COLOR)
        self.__playerFrame.grid(row=1, column=0, padx=5, pady=5)
        self.__dealerFrame.grid(row=1, column=1, padx=5, pady=5)
        self.__pCanvas.grid(row=0, column=0)
        self.__dealerCanvas.grid(row=0, column=0)

        self.__buttonFrame = tk.LabelFrame(
            wn, text='Actions', width=50, height=50)
        self.__buttonFrame.grid(
            row=2, column=0, columnspan=2, padx=5, pady=5)

        self.__btnNewGame = tk.Button(
            self.__buttonFrame, text="New Game", command=self.setupGame)
        self.__btnNewGame.grid(row=0, column=0, padx=2)

        self.__btnStand = tk.Button(
            self.__buttonFrame, text="Stand", command=self.stand, state='disabled')
        self.__btnStand.grid(row=0, column=1, padx=2)

        self.__btnHit = tk.Button(self.__buttonFrame, text="Hit", command=lambda: self.hit(
            self.__player), state='disabled')
        self.__btnHit.grid(row=0, column=2, padx=2)

        self.__btnDoubleDown = tk.Button(
            self.__buttonFrame, text="Double Down", command=self.doubleDown, state='disabled')
        self.__btnDoubleDown.grid(row=0, column=3, padx=2)

        self.__textFrame = tk.LabelFrame(
            wn, text='Outcome', bd=0, height=50, padx=10, pady=10, labelanchor='n')
        self.__textFrame.grid(row=3, column=0, columnspan=2,
                            padx=5, pady=5)

        self.__outcomeLabel = tk.Label(
            self.__textFrame, text="", font=("Arial", 14),width=50)
        self.__outcomeLabel.pack()

    def setupGame(self) -> None:
        """
        Sets up the blackjack game.
        - Shuffles deck
        - Deals hand to player and dealer
        - Enables buttons
        - Renders card
        - Checks for bust off rip
        """
        self.reset()

        self.__blackjackDeck.shuffle()

        self.setHand(self.__player)

        self.setHand(self.__dealer)

        self.__btnHit.config(state='normal')
        self.__btnStand.config(state='normal')
        self.__btnDoubleDown.config(state='normal')

        self.render()

        if self.__player.bust():
            self.busted(self.__player.name)

    def setHand(self, player: BP) -> None:
        """
        Sets the given players hand by dealing them two cards

        :param player: Player to set hand for
        :type player: BP
        """
        for _ in range(2):
            card = self.__blackjackDeck.dealCard()

            player.addCard(card)
            player.addToValue(card.getValue())

    def hit(self, player: BP) -> None:
        """
        Deals the given player a card. If the given player is the user, this checks if they bust after hitting. 

        :param player: Player to deal card to
        :type player: BP
        """
        self.disable_buttons()

        card = self.__blackjackDeck.dealCard()

        player.addCard(card)
        player.addToValue(card.getValue())

        self.__outcomeLabel.config(text=f'{player.name} hit and got a {card}')

        self.render()

        # Check for user bust
        if player.name == 'Player' and player.bust():
            self.__gameOver = True
            self.__pCanvas.after(DELAY_SEC, self.busted, player.name)
        elif not self.__dealerTurn:
            self.enable_buttons()

    def stand(self, msg: str='User stands...') -> None:
        """
        User stands, and the dealer is dealt cards until their hand value is greater than 17.  

        :param msg: Message to display, defaults to 'User stands...'
        :type msg: str      
        """
        self.disable_buttons()

        self.__outcomeLabel.config(
            text=msg, fg=TEXT_COLOR_DEFAULT)

        self.__dealerTurn = True

        self.__dealerCanvas.delete(tk.ALL)
        self.render()

        self.__dealerCanvas.after(DELAY_SEC, self.dealer_turn_step)

    def dealer_turn_step(self) -> None:
        """
        Recursively deals the dealer a card every `DELAY_SEC` until their hand value is greater than 17.
        If it it, this checks for a bust
        or if its time to compare with the users deck.
        """
        if self.__dealer.getTotalValue() < 17:
            self.hit(self.__dealer)

            self.render()

            # Schedule the next step
            self.__dealerCanvas.after(DELAY_SEC, self.dealer_turn_step)
        else:
            # Check for bust else compare decks
            if self.__dealer.bust():
                self.__dealerCanvas.after(
                    DELAY_SEC, self.busted, self.__dealer.name)
            else:
                self.__dealerCanvas.after(DELAY_SEC, self.compare_decks)

    def doubleDown(self) -> None:
        """
        User doubles down. Deals a card to user and then goes to the dealers turn.
        """
        self.disable_buttons()

        self.hit(self.__player)

        if not self.__gameOver:
            self.stand("User doubles down...")

    def busted(self, name: str) -> None:
        """
        Displays a message indicating the given `name` busted and then ends the game.
        """
        if name == 'Dealer':
            self.__outcomeLabel.config(
                text='The Dealer busted! You win!', fg=TEXT_COLOR_GOOD)
        elif name == 'Player':
            self.__outcomeLabel.config(
                text='You busted! You lose...', fg=TEXT_COLOR_BAD)

        self.disable_buttons()

    def compare_decks(self) -> None:
        """
        Compares the players and dealers decks to determine a tie or who won.
        """
        p_value = self.__player.getTotalValue()
        d_value = self.__dealer.getTotalValue()

        if p_value == d_value:
            self.__outcomeLabel.config(
                text=f'You and the dealer push with {self.__player.getTotalValue()}.', fg=TEXT_COLOR_DEFAULT)
        elif p_value > d_value:
            self.__outcomeLabel.config(
                text=f'The dealer got {d_value}, you win with {p_value}!', fg=TEXT_COLOR_GOOD)
        else:
            self.__outcomeLabel.config(
                text=f'The dealer got {d_value}, you lose with {p_value}', fg=TEXT_COLOR_BAD)

        self.disable_buttons()

    def reset(self) -> None:
        """
        Resets the game by reinitializng dealer and player, resetting blackjack deck, and some other variables
        """
        self.__player = BP('Player')
        self.__dealer = BP('Dealer')
        self.__blackjackDeck.reset()
        self.__gameOver = False
        self.__dealerTurn = False
        self.__outcomeLabel.config(text="", fg=TEXT_COLOR_DEFAULT)

    def render(self) -> None:
        """
        Renders the blackjack game to the dealer and player canvas'.
        """
        self.__dealerCanvas.delete(tk.ALL)

        phand = self.__player.getHand()
        dhand = self.__dealer.getHand()

        self.__pCanvas.delete(tk.ALL)

        # Draw Player hand
        counter = 1
        for card in phand:
            card.draw(self.__pCanvas, top=10, left=10 * counter)
            counter += 2

        # Reveal cards if dealers turn
        if not self.__dealerTurn:
            # Dealers Hand
            DC.backOfCard.draw(self.__dealerCanvas, top=10,
                               left=10)  # type: ignore
            dhand[1].draw(self.__dealerCanvas, top=10, left=30)
        else:
            # Draw Dealer hand
            counter = 1
            for card in dhand:
                card.draw(self.__dealerCanvas, top=10, left=10 * counter)
                counter += 2

    def disable_buttons(self) -> None:
        """
        Disable user options
        """
        self.__btnHit.config(state='disabled')
        self.__btnStand.config(state='disabled')
        self.__btnDoubleDown.config(state='disabled')

    def enable_buttons(self) -> None:
        """
        Enable user options
        """
        self.__btnHit.config(state='normal')
        self.__btnStand.config(state='normal')
        self.__btnDoubleDown.config(state='normal')
