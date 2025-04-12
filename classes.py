import random as r
from functions import *

class Kel():
    """Provides methods simulating Kel's thoughts and guesses. Also stores Kel's dialogue and provides methods to access it."""
    def __init__(self):
        # Variables relevant to guess information
        self.guesses = []
        self.guess_results = []
        self.syl_count = r.randint(1, 4)
        self.first_letter_found = False
        self.first_letter = 'a'
        self.num_parts_list = [[1], [1,2], [1,2,3], [2,3,4], [2,3,4], [2,3,4], [3,4], [3,4], [3,4], [4],[4],[4]]

        # Dialogue
        # Greetings:
        self.greetings = ['Welcome, friend! Let us play.',
                          'I hope you are prepared to die.',
                          'It has been too long. Too long indeed!',
                          'Another soul to challenge me.',
                          'Maybe this one will prove better than the last.',
                          'Are you prepared to die?',
                          'Welcome, traveler.',
                          'The names of Kleiast await.',
                          'Was your journey long?']
        
        # Goad response (low anger):
        self.goad_responses_low = ['It is not wise to goad me.',
                                  'Is that so? We shall see. We shall see.',
                                  '...',
                                  'Do not try me.',
                                  'A little luck goes a long way.',
                                  'Truly?',
                                  'Are you certain?',
                                  'The stone chooses who it wills. Next time it may not choose you.']

        # Goad responce (high anger):
        self.goad_responses_high = ['Try me again, and see where that gets you.',
                                   'You know not of which you speak.',
                                   'I will enjoy ending you.',
                                   'Are you so sure?']

        # Blaspheme reaction:
        self.death_messages = ['Where is your respect?',
                              'You lack wisdom.',
                              'I do not play with idiots.',
                              'You have wasted your chance.',
                              'You have offended the spirits.',
                              'A shame.',
                              'If you will not show respect, neither shall I.',
                              'Insolence!',
                              'Blasphemer!',
                              'Return to whence you came.',
                              'May your voice never ring in this hall again.']

        # Kel wins
        self.wins = ['I win.',
                     'Thus speak the spirits.',
                     'A fair game.',
                     'Welcome to Kleiast, my friend.',
                     'Alas. Your spirit was not in tune.', 
                     'I have bested you. Your blood is mine.',
                     'You were far from the truth.', 
                     'It is time to pay the price.', 
                     'Farewell, friend. Send another.']
        
        # Accepting higher stakes (low anger):
        self.accepts_low = ['I accept.',
                           'A fair bargain. I accept.',
                           'Let us see if your soul holds true. I accept.',
                           'Intriguing. I accept.',
                           'I accept. Let us play.']

        # Accepting higher stakes (high anger):
        self.accepts_high = ['I accept your challenge.',
                            'You will regret this. I accept.',
                            'You press your luck, but I care not. I accept.']
        
        # Rejecting higher stakes (high anger):
        self.rejects = ['No. Leave this place.',
                       'No. Take your winnings and begone.',
                       'I refuse. But I await your return eagerly.',
                       'I refuse. You have bested me.',
                       'No. But I will have your blood someday.',
                       'No. You will pay for this.']

        # Reactions
        self.reactions = ["[Kel's eyes sparkle.]",
                          "[A smile twists the edge of Kel's mouth.]",
                          "[Kel looks into your eyes.]",
                          "[Kel clasps his hands.]",
                          "[Kel's eyes shine in the darkness.]",
                          "[Kel drums his fingers on the stone.]"]

        # Kel loses
        self.loss = ["You play well.",
                     "Well played.",
                     "You know your names.",
                     "A fair victory.",
                     "I should have known.",
                     "Klast.",
                     "Hmm...",
                     "Interesting...",
                     "Intriguing...",
                     "I was farther from the truth than I thought."]

    # Guess methods
    def answer(self, answer_key):
        """Stores the answer_key for later use."""
        self.answer_key = answer_key        
    
    def store(self, prev_guess, result):
        """Accepts the previous guess (string) and the stone's output (int) and stores it for Kel's use."""
        self.guesses.append(prev_guess)
        self.guess_results.append(result)

    def gen_1st_syl(self):
        """Uses self.first_letter to generate a valid syllable. Returns a string."""
        # Don't do anything if there's no first letter
        if self.first_letter_found == False:
            return ''
            
        syl = self.first_letter
        # Add a vowel/diphthong if necessary
        if self.first_letter not in 'aei':
            syl += r.choices(['a', 'e', 'i', 'ai', 'ei'])[0]
        # Add an ending cluster 
        syl += r.choices(['', 'r', 'h', 's', 'l', 'sh', 'st', 'sht', 'th'])[0]
        return syl

    def guess_syl(self):
        """Updates Kel's guess of how many syllables are in the word."""
        # Don't do anything on the 2nd guess - syl_count has already been initialized
        if len(self.guesses) == 1:
            return

        # If a guess has been good, copy that one maybe plus or minus one syllable
        best_guess = max(self.guess_results)
        if best_guess >= 3:
            self.syl_count = count_syl(self.guesses[self.guess_results.index(best_guess)])
            if best_guess == 3:
                rand = r.randint(1, 3)
                if rand == 1:
                    self.syl_count -= 1
                elif rand == 2:
                    self.syl_count += 1
        # Else if syl_count is low, Kel suspects this word is longer
        elif self.syl_count < 4:
            self.syl_count += r.randint(1, 3)
        # Else, Kel suspects the word is shorter
        else:
            self.syl_count -= r.randint(1, 3)

    def guess_1st(self):
        """Updates Kel's guess of what the first letter of the word is."""
        best_guess = max(self.guess_results)
        # Check if Kel has already guessed a first letter (never true for the 2nd guess)
        if self.first_letter_found:
            # If the player's guess was the same or better than Kel's old guess, 
            # and the 1st letter was different, forget the chosen letter.
            if (self.guess_results[-2] <= self.guess_results[-1]) ^ (self.first_letter[0] != self.guesses[-1][0]):
                self.first_letter_found = False
        
        # If a guess has been good, copy its 1st letter
        if best_guess >= 3:
            self.first_letter_found = True
            self.first_letter = self.guesses[self.guess_results.index(best_guess)][0]
            # If it's a consonant cluster, copy the 2nd letter also
            if self.guesses[self.guess_results.index(best_guess)][1] in 'hlr':
                self.first_letter += self.guesses[self.guess_results.index(best_guess)][1]

    def get_close(self):
        """If a guess has been very close, simulate Kel guessing very close to the answer by using the answer key. 
        Generates a guess and returns a string."""
        guess = ''
        remaining = len(answer_key)
        error = 5
        # If the word is short, don't put in any hyphens
        if remaining < 3:
            for i in range(remaining):
                part = syl_vec[r.randint(answer_key[i]-error, answer_key[i]+error)]
                guess += part
            return fix_word(guess)

        # If the word is longer, string together parts with hyphens
        num_parts = r.choices(self.num_parts_list[remaining-1])[0]
        
        for i in range(num_parts):
            part = ''
            if remaining == 0:
                if guess.endswith('-'):
                    guess = guess.rstrip('-')
                break
            if i == num_parts - 1:
                # Last part must have remaining syllables
                for j in range(remaining):
                    part = syl_vec[r.randint(answer_key[i]-error, answer_key[i]+error)]
                    guess += part
            else:
                # First/middle parts can have 1-3 syllables
                rand = r.randint(1, 3)
                for j in range(rand):
                    part += syl_vec[r.randint(answer_key[i]-error, answer_key[i]+error)]
                remaining -= count_syl(part)
                guess += (part + '-')
                
        # Fix the word
        return fix_word(guess)

    def guess(self):
        """Generates a guess. Returns a string."""
        guess = ''

        # Check how well the size of the previous answer worked
        if self.guess_results[-1] == 5:
            return self.get_close()
        else:
            # Update Kel's guesses
            self.guess_1st()
            self.guess_syl()

        if self.syl_count == 1:
            if self.first_letter_found:
                return self.gen_1st_syl()
            else: 
                return generate_word(syl_vec, 1, [1])
        
        # Generate a word with syl_count - 1 syllables
        # Pick a number of parts 
        num_parts = r.choices(self.num_parts_list[self.syl_count-2])[0]

        # KNOWN BUG - the below loop only works correctly if remaining is 3 or greater. Currently has a chance
        # to generate 4 syllable words without a break if a 3 is chosen in the 'else' block
        # Stitch together a word with the correct number of parts and syllables
        remaining = self.syl_count - 1
        for i in range(num_parts):
            part = ''
            if remaining <= 0:
                if guess.endswith('-'):
                    guess = guess.rstrip('-')
                break
            if i == num_parts - 1:
                # Last part must have remaining syllables
                part = generate_word(syl_vec, 1, [remaining])
                guess += part
            else:
                # Middle parts can have 1-3 syllables
                part = generate_word(syl_vec, 1, [r.randint(1, 3)])
                remaining -= count_syl(part)
                guess += (part + '-')

        # Add 1st syllable 
        # If the guess is already 3 syllables, and Kel is generating a 1st syllable, add a hyphen
        if count_syl(guess) == 3 and self.first_letter_found:
            guess = self.gen_1st_syl() + '-' + guess
            return guess

        guess = self.gen_1st_syl() + guess

        # Fix the word
        return fix_word(guess)

    # Dialogue methods
    def greet(self):
        num = r.randint(0, len(self.greetings)-1)
        return self.greetings[num]

    def respond_low(self):
        num = r.randint(0, len(self.goad_responses_low)-1)
        return self.goad_responses_low[num]

    def respond_high(self):
        num = r.randint(0, len(self.goad_responses_high)-1)
        return self.goad_responses_high[num]

    def death_message(self):
        num = r.randint(0, len(self.death_messages)-1)
        return self.death_messages[num]

    def win(self):
        num = r.randint(0, len(self.wins)-1)
        return self.wins[num]

    def accept_low(self):
        num = r.randint(0, len(self.accepts_low)-1)
        return self.accepts_low[num]

    def accept_high(self):
        num = r.randint(0, len(self.accepts_high)-1)
        return self.accepts_high[num]

    def reject(self):
        num = r.randint(0, len(self.rejects)-1)
        return self.rejects[num]

    def reaction(self):
        num = r.randint(0, len(self.reactions)-1)
        return self.reactions[num]

    def lose(self):
        num = r.randint(0, len(self.loss)-1)
        return self.loss[num]


# Player - CURRENTLY UNUSED
class Player():
    """Stores the player's dialogue and provides methods to access it."""
    def __init__(self):
        # Goads
        self.goads = ['That was too easy.',
                      'This game is for children.',
                      'That was all?',
                      'I am not afraid of you.',
                      'Looks like the stone chose me.',
                      'I think I heard that name, once.',
                      "You're quite bad at this for having played so long.",
                      "Beginner's luck, huh?",
                      'Humanity wins again.',
                      'Some spirits in that rock, eh?',
                      'I conquered your haunted rock.',
                      'Like a cool summer breeze.']

    def goad(self):
        num = r.randint(0, len(self.goads)-1)
        print(self.goads[num])








