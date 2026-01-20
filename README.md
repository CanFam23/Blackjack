# Blackjack

A Python-based Blackjack game using TKinter. 

I wanted to refresh my Python GUI skills and what better way to do so than recreating one of my first Python projects?

## House Rules (Features)
Since it was so easy to recreate, my Blackjack has special rules:
1. Aces are always low (1, no exceptions)
2. No splitting
3. Dealer stands on 17 or higher

## Betting Opportunities

If you want to play with real money email me your credit card information and I will track your betting manually...

Unfortunately I'm joking don't do this.

# Prerequisites

* Python installed on your device.
  * I developed this with Python 3.10.6, and it **has not been tested with other versions**.
# Setup

## Virtual Environment (Optional)

If you want to set up a virtual environment, follow these steps:  
1. Open a terminal and navigate to the location you'd like it to be created.

2. Create a new venv (replace `venv_name` with your preferred name):

```bash
$ python3 -m venv venv_name
```

3. Activate the venv:

```bash
$ source path/to/venv/venv_name/bin/activate
```

Successful activation will show the venv name next to the terminal cursor:

```bash
(venv_name) $ _
```

## Install requirements

1. Navigate to the root directory of the project, then install the libraries in the `requirements.txt` file:

```bash
$ pip install -r requirements.txt
```

# Running the game

To run the game through a terminal, type:

```bash
python main.py
```

Or `python3` if `python` doesn't work.

Once running, a Python GUI should display in the center of your screen.

# Known Issues / Limitations

* Only tested with Python 3.10.6. Other versions may not work correctly.

# Shoutout
Shoutout to Ted Wendt for the `DeckOfCards.py`, `Card.py`, and `deck_of_cards.png` files.