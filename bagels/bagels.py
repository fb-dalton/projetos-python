'''Bagels, a deductive logic game.
By Al Sweigart al@inventwithpython.com'''

import random
from validation import data_validation

print('I am thinking of a 3 number digit between 100 and 999. Try to guess what it is.')
secret_number = str(random.randint(100, 999))

print('''Here are some clues:
When I say:    That means:
Pico           One digit is correct but in the wrong position.
Fermi          One digit is correct and in the right position.
Bagels         No digit is correct.
I have thought up a number.
 You have 10 guesses to get it.''')
list_of_guesses = []
guess_count = 0
guess = ''
while guess_count < 10:
    guess = data_validation.validate_str(input('Enter a guess: '))
    list_of_guesses.append(guess)
    if guess == secret_number:
        print(f'You got it! The answer was {secret_number}!')
        break
    else:
        result = data_validation.validate_rng(secret_number, guess)
        for c in result:
            print(c, end=' ')
        print('')
    guess_count += 1
    if guess_count == 10:
        print(f'You are out of guesses. The answer was {secret_number}.')
print('Thanks for playing!')