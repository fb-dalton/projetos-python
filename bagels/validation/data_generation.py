import random
def uniq_3():
    digits = list('0123456789')
    random.shuffle(digits)
    return ''.join(digits[:3])