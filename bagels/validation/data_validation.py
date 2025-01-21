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
    '''
    num - number to guess
    guess - user's guess
    Verify if there are correct numbers in the correct or wrong position and return a flag without specifying the number or position'''
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

