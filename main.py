from time import sleep
from functions import *
from classes import *
from dependent_functions import *

# Set time step 
d = 1.2

# Create classes for use
kel = Kel()
player = Player()
    
# The game

# Title screen/Instructions
print("KEL, DEMON OF NAMES\n")

print("Welcome, guardian.\n")

intro = True
game = False
while intro:
    inputStr = opening()

    # Print instructions
    if (inputStr == "1"):
        instructions()

    # Continue to the game
    elif (inputStr == "2"):
        print("[You have entered Kel's domain.]\n")
        sleep(d)
        kel_says(kel.greet())
        sleep(d)
        intro = False
        game = True

    # Quit
    elif (inputStr == "3"):
        intro = False

    # Quit
    elif (inputStr == "quit"):
        intro = False

# Gameplay
while game:
    # Initialize variables
    name, answer_key = generate_name(syl_vec)
    kel.answer(answer_key)

    # Start
    print('[Kel smiles.]')
    sleep(d)
    kel_says('Write your word.\n')
    sleep(d)

    # Get player's guess
    guess1 = input()
    guess1 = str(validate(guess1))

    print('')

    # Quit/die
    if guess1 == 'quit':
        game = False 
        break
    elif guess1 == '0':
        die(0)
        game = False
        break

    # Get stone's reaction
    sleep(d)
    react1 = stone(guess1, name) 
    kel.store(guess1, react1)
    sleep(d)

    # Instant win if the word is correct
    if react1 == 6:
        kel_says(kel.lose())
        game = False
        break

    # Kel's guess 
    guess2 = kel.guess()
    guess2 = guess2.capitalize()
    kel_says(guess2 + '.')
    print('')
    sleep(d)

    # Get stone's reaction
    react2 = stone(guess2, name)
    kel.store(guess2, react2)
    sleep(d)

    # Instant loss if the word is correct
    if react2 == 6:
        die(1)
        game = False
        break
    
    # Get player's guess
    guess3 = input()
    guess3 = str(validate(guess3))

    print('')

    # Quit/die
    if guess3 == 'quit':
        game = False 
        break
    elif guess3 == '0':
        die(0)
        game = False
        break

    # Get stone's reaction
    sleep(d)
    react3 = stone(guess3, name)
    kel.store(guess3, react3)
    sleep(d)

    # Instant win if the word is correct
    if react3 == 6:
        kel_says(kel.lose())
        game = False
        break

    # Kel reacts
    print(kel.reaction() + '\n')
    sleep(d)

    # Kel's guess 
    guess4 = kel.guess()
    guess4 = guess4.capitalize()
    kel_says(guess4 + '.')
    print('')
    sleep(d)

    # Get stone's reaction
    react4 = stone(guess4, name)
    kel.store(guess4, react4)
    sleep(d)

    # Instant loss if the word is correct
    if react4 == 6:
        die(1)
        game = False
        break

    # Get player's guess
    guess5 = input()
    guess5 = str(validate(guess5))

    print('')

    # Quit/die
    if guess5 == 'quit':
        game = False 
        break
    elif guess5 == '0':
        die(0)
        game = False
        break

    # Get stone's reaction
    sleep(d)
    react5 = stone(guess5, name)
    kel.store(guess5, react5)
    sleep(d)

    # Instant win if the word is correct
    if react5 == 6:
        kel_says(kel.lose())
        game = False
        break

    # Kel's guess
    guess6 = kel.guess()
    guess6 = guess6.capitalize()
    kel_says(guess6 + '.')
    print('')
    sleep(d)

    # Get stone's reaction
    react6 = stone(guess6, name)
    kel.store(guess6, react6)
    sleep(d)

    # Instant loss if the word is correct
    if react6 == 6:
        die(1)
        game = False
        break

    # Kel says something about the final guess
    print(kel.reaction())
    sleep(d)
    kel_says('It is time. Write your final word.')
    sleep(d)
    print('')

    # Get player's final guess
    p_guess = input()
    p_guess = str(validate(p_guess))

    print('')

    # Quit/die
    if p_guess == 'quit':
        game = False 
        break
    elif p_guess == '0':
        die(0)
        game = False
        break
    
    sleep(d)

    # Get Kel's final guess
    k_guess = kel.guess()
    k_guess = k_guess.capitalize()
    kel_says(k_guess + '.')
    print('')
    sleep(d)

    # Get the stone's judgement
    outcome = stone2(p_guess, k_guess, name)
    
    # Lose
    if outcome == 1:
        die(1)
        game = False
        break

    # Draw
    elif outcome == 2:
        kel_says('...That was unexpected. Draw.')
        game = False
        break 
        
    # Win
    kel_says(kel.lose())
    sleep(d)
    print('[You have won the contest.]')
    
    # TO ADD - Bartering portion

    break
    
    
