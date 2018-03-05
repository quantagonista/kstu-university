import numpy as np

SIZE = 5


def build_magic_square(SIZE):
    magic_square = np.eye(SIZE, dtype=int)
    for i in range(SIZE):
        for j in range(SIZE):
            magic_square[i][j] = 1 + ((i + j - 1 + (SIZE - 1) / 2) % SIZE) * SIZE + ((i + 2 * j + 2) % SIZE)
    magic = []
    for i in range(SIZE):
        for j in range(SIZE):
            magic.append(magic_square[i][j])
    return magic


def build_string_square(string):
    string_square = np.eye(SIZE, dtype=str)
    index = 0
    for i in range(SIZE):
        for j in range(SIZE):
            string_square[i][j] = string[index]
            index += 1
    return string_square


def encrypt(string):
    checked_string = check_length(string, SIZE ** 2)
    secret_ingredient = build_magic_square(SIZE)
    encrypted_string = do_magic(checked_string, secret_ingredient)
    print(encrypted_string)
    return encrypted_string

def decrypt(string):
    magic = build_magic_square(SIZE)
    do_magic_again(string, magic)
    print()


def do_magic(string, magic):
    encrypted_string = ''
    for i in range(len(string)):
        encrypted_string += string[magic[i] - 1]
    return encrypted_string


def do_magic_again(string, magic):
    index = 0
    decrypted_string = ''
    decrypted_hash = {}
    for i in magic:
        decrypted_hash[i] = string[index]
        index += 1
    for key in sorted(decrypted_hash):
        decrypted_string += decrypted_hash[key]
    print(decrypted_string)


def check_length(string, length):
    if len(string) == length:
        return string
    elif len(string) < length:
        X = "X" * (length - len(string))
        result_string = string + X
        return result_string
    else:
        return str(string)[:length]


def encrypt_by_block(source_string, size=5):
    string = source_string
    encrypted_string = ''
    str_len = size ** 2
    iterator = 0
    while iterator <= len(string):
        temp = string[iterator:str_len]
        encrypted_string += encrypt(temp)
        iterator += str_len + 1
        str_len += str_len + 1
    print (encrypted_string)


poem = """And what is love? It is a doll dressed up
For idleness to cosset, nurse, and dandle;
A thing of soft misnomers, so divine
That silly youth doth think to make itself
Divine by loving, and so goes on
Yawning and doting a whole summer long,
Till Miss's comb is made a perfect tiara,
And common Wellingtons turn Romeo boots;
Till Cleopatra lives at Number Seven,
And Antony resides in Brunswick Square."""

encrypt_by_block(poem)
