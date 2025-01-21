'''Bagels, a deductive logic game.
By Al Sweigart al@inventwithpython.com'''

from validation import data_validation, data_generation

print('I am thinking of a 3 number digit. Try to guess what it is.')
secret_number = data_generation.uniq_3() # this generate a 3 digit number with 3 unique digits.

print('''Here are some clues:
When I say:    That means:
Pico           One digit is correct but in the wrong position.
Fermi          One digit is correct and in the right position.
Bagels         No digit is correct.
I have thought up a number.
You have 10 guesses to get it.''')
list_of_guesses = []
max_guesses = 10 #maximum number of guesses
guess_count = 0
guess = ''
#main loop, where the user guesses the number
while guess_count < max_guesses: 
    # this validate if the number is 3-digit and numeric.
    guess = data_validation.validate_str(input('Enter a guess: ')) 
    list_of_guesses.append(guess)
    #this checks if the guess is correct
    if guess == secret_number:
        print(f'You got it! The answer was {secret_number}!')
        break
    else:
        #this compares the guess with the secret number and returns the clues 
        result = data_validation.validate_rng(secret_number, guess)
        for c in result:
            print(c, end=' ')
        print('')
    #count the number of guesses
    guess_count += 1 
    #verify if the user runs out of guesses
    if guess_count == max_guesses: 
        print(f'You are out of guesses. The answer was {secret_number}.')
print('Thanks for playing!')