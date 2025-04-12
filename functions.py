import numpy as np
import random as r
from time import sleep

# Time step 
d = 1.2

# Point values
CORRECT_SYL = 150
CORRECT_LEN = 200
CORRECT_LOC = 200
CORRECT_LET = 50
BAD_LET = 100
CORRECT_HYP = 100
CORRECT_1ST = 200

# Create a vector of syllables
with open('Syllables3.txt', 'r') as file:
    syl_vec = [line.strip() for line in file]

# Fix the first element 
syl_vec[0] = 'a'

def inputLoop(*args):
    """Accepts strings as arguments, prints them in the appropriate format, validates player input, 
    and returns a string of the user input."""
    loop = True
    options = ""
    while loop:
        print("Choose an action:")
        for i, ar in enumerate(args):
            # Count the viable options
            options = options + str(i + 1)
            print(str(i + 1) + " - " + ar)

        print("")

        inputStr = input()

        print("")
            
        if inputStr == "quit":
            loop = False
            return "quit"
            
        elif inputStr in options:
            loop = False
            return inputStr
            
        else:
            print("Invalid input.")
            sleep(d)

def opening():
    """Prints the title of the game, opening dialogue, and returns the player's input.""" 
    sleep(d)
    print("Input a number to select an action. Type 'quit' at any time to quit.\n")

    inputStr = inputLoop("Instructions", "Challenge Kel", "Quit")
    return inputStr

def instructions():
    """Prints the instructions of the game."""
    print("You have chosen to challenge Kel, the Demon of Names.")
    print("Kel's hatred for mankind is unending, as with all demons.")
    print("However, his game gives him more pleasure than killing humans outright.")
    print("Ancient guardians bound Kel by an immutable covenant: if a human wins his game, Kel must remain dormant for a period of time.")
    print("If Kel wins, he may slay the one who challenged him and immediately request a rematch.")
    print("Kel is cunning, but he will always abide by the rules of his game.\n")
    sleep(d)
    print("Each game, spirits within the stone before Kel will choose a name.")
    print("The object of the game is to guess as close as possible to the stone's name.")
    print("You and Kel will each guess three times, one after the other, writing your guess on the stone.")
    print("You must write carefully. If you write characters that are not acceptable, you blaspheme the stone, and Kel will kill you.")
    print("The stone will react to your guess, shining brighter the closer your guess is to the true name.")
    print("After each guessing three times, you and Kel will write your final guesses at the same time.")
    print("The stone will reveal the name and indicate the winner.\n")
    sleep(d)
    print("Previous guardians have recorded information about the language these spirits speak:")
    print("The following letters have never occurred in a true name: q, w, y, u, o, p, d, f, g, j, z, x, c, b, m.")
    print("Note that the only acceptable vowels are a, e, and i. The only diphthongs that have appeared are 'ai' and 'ei'.")
    print("A word may consist of parts one to three syllables long connected by hyphens.")
    print("A word may consist of up to four parts. This is extremely rare, however. Most often they have one or two.")
    print("It is common for syllables to end in 'st', 'th', and 'sht'.")
    print("It is common for the second letter of a syllable to be r or l.")
    print("It is common for a syllable to start with h, k, v, or t. When in doubt, go with these.\n")
    sleep(d)
    print("Good luck, guardian.\n")
    sleep(d)

def kel_says(string):
    """Prints Kel's dialogue."""
    print('[Kel:]', string)

def validate(word):
    """Return '0' if input is invalid, otherwise convert to lowercase and return."""
    # Word should be only letters and hyphens and possibly a period
    if word.count('.') > 0:
        if word.count('.') > 1:
            return "0"
        elif not word.endswith('.'):
            return "0"
        else:
            word = word.rstrip('.')
    no_hyp = word.replace('-', 'a')
    if not no_hyp.isalpha():
        return "0"

    # Word can't start or end in hyphens
    if word.endswith('-'):
        return "0"

    if word.startswith('-'):
        return "0"
        
    word = np.strings.lower(word)

    return word

def get_letters_vec(word):
    """Helper function for get_dict(). Generates a list of each unique letter in the word."""
    letters_vec = ['']
    for letter in word:
        add = True
        for i in range(len(letters_vec)):
            if letters_vec[i] == letter:
                add = False
        if add:
            letters_vec.append(letter)
    letters_vec.remove('')
    return letters_vec

def get_dict(word):
    """Helper function for score(). Returns a dictionary whose keys are the unique letters in the word
    and whose values are lists of indeces corresponding to the location of those letters in the word."""
    letters_vec = get_letters_vec(word)
    dict = {}
    for i in range(len(letters_vec)):
        positions = [0]
        for j in range(word.count(letters_vec[i])):
            positions.append(word.find(letters_vec[i], positions[j]+1))
        if word[0] == letters_vec[i]:
            positions.remove(-1)
        else:
            positions.remove(0)
        dict[letters_vec[i]] = positions
    return dict

def count_syl(word):
    """Helper function for score(). Counts the number of correct syllables in a word and returns an int."""
    ai = word.count('ai')
    ei = word.count('ei')
    a = word.count('a')
    e = word.count('e')
    i = word.count('i')

    syl = ai + ei + (a - ai) + (e - ei) + (i - ai - ei)
    return syl
    
    
def get_score(word, answer):
    """Calculate a score based on the first word's validity in the language and how close it is to the second word."""
    score = 0
    bad_letters = 'qwyupodfgjzxcbm'

    # If the words are the same, win
    if (word == answer):
        score = 99999
        return score

    # For each unique letter, find their positions in 'answer' and store them in answer_dict
    answer_dict = get_dict(answer)
    
    # For each unique letter, find their positions in 'word' and store them in word_dict
    word_dict = get_dict(word)

    # Award points for correct number and type of syllables
    if count_syl(word) == count_syl(answer):
        score += CORRECT_SYL
    
    # Award points for correct word length
    if len(word) == len(answer):
        score += CORRECT_LEN

    # Award/subtract points for letter kinds and positions
    correct_loc = 0
    for letter in list(word_dict):       
        # Subtract points if the letter doesn't exist in the language 
        if letter in bad_letters:
            score -= BAD_LET
            
        # Award points if the letter is in the word or in the right position
        if letter in list(answer_dict):
            word_pos = word_dict[letter]
            ans_pos = answer_dict[letter]
            
            # Special case: hyphens - extra points for correct number of these
            if letter == "-":
                if len(word_pos) == len(ans_pos):
                    score += CORRECT_HYP
                    
            # Iterate through word_pos and award points for correct letter locations
            for i in range(len(word_pos)):
                if word_pos[i] in ans_pos:
                    correct_loc += 1
                    score += CORRECT_LOC
                    # Hyphens - double points
                    if letter == '-':
                        score += CORRECT_LOC
                        
            # Award points for the rest of this letter in incorrect positions (not for hyphens)
            if letter != '-':
                if len(word_pos) < len(ans_pos):
                    score += (len(word_pos) - correct_loc) * CORRECT_LET
                else:
                    score += (len(ans_pos) - correct_loc) * CORRECT_LET
                    

    # In addition to the previous points, add a bonus for getting the first letter correct
    if answer[0] == word[0]:
        score += CORRECT_1ST

    # Subtract points for each letter over the length of the true word + 3
    BAD_LEN = 50
    over = len(word) - (len(answer) + 3)
    if over > 0:
        score -= BAD_LEN * over

    # If a certain number of letters in correct positions has been reached, print this
    if correct_loc > 4:
        print("[The stone flashes bright for just a moment!]")
        sleep(d)
            
    return score

def get_max_score(word):
    """Accepts a string and returns an int which is the maximum score that could be achieved for the given word."""
    dict = get_dict(word)

    max_score = 0

    # Add points for correct number of syllables
    max_score += CORRECT_SYL

    # Add points for correct word length
    max_score += CORRECT_LEN

    # Add points for correct first letter
    max_score += CORRECT_1ST

    # Add points for correct letter positions
    for letter in list(dict):
        # Special case: hyphens
        if letter == "-":
            # Correct number of hyphens
            max_score += CORRECT_HYP
            # Correct position of hyphens - bonus points
            max_score += len(dict[letter]) * CORRECT_LOC * 2

        else:
            # Correct letter positions
            max_score += len(dict[letter]) * CORRECT_LOC

    return max_score

def fix_word(word):
    """Accepts a string and returns a string without undesirable consonant clusters."""
    if 'thth' in word:
        word = word.replace('thth', 'th')
    if 'rr' in word:
        word = word.replace('rr', 'r')
    if 'hh' in word:
        word = word.replace('hh', 'h')
    if 'shsh' in word:
        word = word.replace('shsh', 'sh')
    if 'tt' in word: 
        word = word.replace('tt', 't')
    if 'ss' in word:
        word = word.replace('ss', 's')
    if 'll' in word:
        word = word.replace('ll', 'l')
    if 'aa' in word:
        word = word.replace('aa', 'a')
    if 'ee' in word:
        word = word.replace('ee', 'e')
    if 'ii' in word:
        word = word.replace('ii', 'i')
    
    return word

def generate_word(syl_vec, num_parts, parts_length):
    """Accepts the vector of syllables (and optionally the number of parts and as input and returns a randomly generated word."""  
    # Validate input
    if num_parts == None or parts_length == None:
        raise SyntaxError('Must provide both num_parts and parts_length')

    if not (type(num_parts) == int and type(parts_length) == list):
        raise SyntaxError('Incorrect argument types')

    # Fetch syllables and string them together
    word = ''
    for i in range(num_parts):
        for j in range(parts_length[i]):
            word += syl_vec[r.randint(0, len(syl_vec)-1)]
        if i != (num_parts - 1):
            word += '-'

    # Fix malformed words
    return fix_word(word)

def generate_name(syl_vec):
    """Similar to generate_word except this function also returns a list 'answer_key' which contains the indeces of each used syllable."""
    answer_key = []
    
    # Choose num_parts and parts_length randomly
    num_parts = r.choices([1, 2, 3, 4], [50, 40, 7, 3])[0]
    parts_length = r.choices([1, 2, 3], [40, 50, 10], k = num_parts)

    # Fetch syllables and string them together, storing the index of each syllable in answer_key
    word = ''
    for i in range(num_parts):
        for j in range(parts_length[i]):
            rand = r.randint(0, len(syl_vec)-1)
            word += syl_vec[rand]
            answer_key.append(rand)
        if i != num_parts - 1:
            word += '-'

    # Fix malformed words    
    return fix_word(word), answer_key

def stone(input, answer):
    """Accepts two strings as input, prints a response, and returns a int based on the score between them."""
    score = get_score(input, answer)
    max_score = get_max_score(answer)
    out = 0
    
    if score <= 0:
        print('[The stone becomes pitch black.]\n')
        return out
    elif score <= max_score * 0.1: 
        print('[Something flickers deep within the stone.]\n')
        return out + 1
    elif score <= max_score * 0.25:
        print('[A gold shimmer appears, and is gone.]\n')
        return out + 2
    elif score <= max_score * 0.5:
        print('[Light swirls slowly inside the stone.]\n')
        return out + 3
    elif score <= max_score * 0.75:
        print("[The stone flashes considerably.]\n")
        return out + 4
    elif score < max_score:
        print('[Bright streaks of light form like lightning!]\n')
        return out + 5
    else:
        print('[The stone shines blinding like the sun!]\n')
        return out + 6

def stone2(players, kels, answer):
    """Accepts three strings: the player's final guess, Kel's final guess, and the answer. Prints a message and returns an int
    indicating the outcome."""
    player_score = get_score(players, answer)
    kel_score = get_score(kels, answer)
    answer = answer.capitalize()

    print('[The light within the stone spins rapidly.]')
    sleep(d)
    print('[A shape is forming...]')
    sleep(d*2)
    print("[A word appears on the stone:", answer, "]")

    if player_score > kel_score:
        print('[A golden arrow points to you.]')
        sleep(d)
        return 0
    elif kel_score > player_score:
        print('[A golden arrow points toward Kel.]')
        sleep(d)
        return 1
    else:
        print('[A golden bar runs from you to Kel.]')
        sleep(d)
        return 2







