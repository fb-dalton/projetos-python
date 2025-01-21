def validate_size(data):
    '''
    data - user's guess
    Evaluate the size of user's guess and return it'''
    data = data.strip()
    while True:
        if len(data) == 3:
                return data
        else:
            data = input('Try again, wrong length of guess: ').strip()


def validate_str(data):
    '''
    data - user's guess
    Evaluate the type of user's guess and return it'''
    while True:
        data = validate_size(data)
        if data.isdigit():
            return data
        else:
            data = input('Try again, not a number: ').strip()
        

def validate_rng(num, guess):
    """
    Generates the clues for the user (pico, fermi, bagels).
    Pico if the digit is correct but in the wrong position.
    Fermi if the digit is correct and in the right position.
    Bagels if no digit is correct.

    Args:
        num (str): insert a random number generation function that returns a 
        3 unique digit number
        guess (str): number input by user, must be 3 digit number

    Returns:
        'pico', 'fermi', 'bagels': returns the clues for the user
    """
    b = 0
    test = []
    for c in range(3):
        if num[c] in guess:
            test.append('Fermi') if num[c] == guess[c] else test.append('Pico')
        else:
            b += 1
    if b == 3:
        test.append('Bagels')
    return test

