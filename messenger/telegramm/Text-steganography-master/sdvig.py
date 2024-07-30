def encode(word, step):
    new_word = ""
    for i in word:
        new_word += chr(ord(i) + step)
    return new_word

def decode(word, step):
    new_word = ""
    for i in word:
        new_word += chr(ord(i) - step)
    return new_word