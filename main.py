'''
file: main.py 

description: This file serves as the main script of a Blackjack game, 
and is the file you run to play the game.
'''
import tkinter as tk

from blackjack.BlackjackGame import BlackjackGame

if __name__ == '__main__':
    wn = tk.Tk()

    n = BlackjackGame(wn)
    wn.mainloop()