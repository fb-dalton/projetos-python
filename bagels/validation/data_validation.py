def validate_str(data):
    try:
        data = str(data)
    except Exception:
        data = input('Try again, wrong type of guess: ')

    try:
       if data.isnumeric():
           pass
    except Exception:
        data = input('Try again, wrong type of guess: ')
    else:
        return str(data).strip()
    

def validate_rng(num, guess):
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
        