
def encrypt(message, public_key):
    e, n = public_key
    cipher_list = list(map(lambda letter: pow(ord(letter), e, n), message))
    cipher_text = ''
    for i in cipher_list:
        cipher_text += str(i) + ' '

    return cipher_text.strip()


def decrypt(cipher_text, private_key):
    d, n = private_key
    message = list(map(lambda x: int(x), cipher_text.split(' ')))
    decrypted_list = list(map(lambda x: pow(x, d, n), message))
    decrypted_text = ''
    for i in decrypted_list:
        decrypted_text += chr(i)
    return decrypted_text


def generateKeys(primes, e):
    p, q = primes
    n = p*q
    phi = (p-1) * (q-1)
    d = multiplicative_inverse(e, phi)

    public = [e, n]
    private = [d, n]

    return public, private


def multiplicative_inverse(a, b):
    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a  # Remember original a/b to remove
    ob = b  # negative values from return results
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)
    if lx < 0:
        lx += ob  # If neg wrap modulo orignal b
    if ly < 0:
        ly += oa  # If neg wrap modulo orignal a
    # return a , lx, ly  # Return only positive values
    return lx


def gcd(a, b):
    if b:
        return gcd(b, a % b)
    else:
        return a


def main():

    text = "Still not able to restore your session? Sometimes a tab is causing the issue. View previous tabs, remove the checkmark from the tabs you don’t need to recover, and then restore."

    public, private = generateKeys([1277, 1117], 65537)
    print("public: ", public)
    print('private: ', private)

    encrypted = encrypt(text, public)
    decrypted = decrypt(encrypted, private)

    print('encrypted message: ', encrypted)
    print('decrypted message: ', decrypted)


main()
