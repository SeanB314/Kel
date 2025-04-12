"""dependent_functions contains all the functions that require the Kel class to be defined."""
from time import sleep
from functions import kel_says
from classes import Kel

# Time step
d = 1.2

# Create classes for use
kel = Kel()

def die(type):
    """Print the dialogue for losing the game. Accepts an int signifying the type of death."""
    # Blasphemy death
    if type == 0:
        kel_says(kel.death_message())
        sleep(d)
    # Kel wins
    elif type == 1:
        kel_says(kel.win())
        sleep(d)
        
    print('[*SKLAT*]')
    sleep(d)
    print('[You have been slain by Kel.]')

