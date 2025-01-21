import random
def uniq_3():
    """generates a 3 digit number with 3 unique digits, in str format.
    """
    digits = list('0123456789')
    random.shuffle(digits)
    return ''.join(digits[:3])