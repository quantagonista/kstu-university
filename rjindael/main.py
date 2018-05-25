import constants as c
from galua_ops import *


class AES():
    def __init__(self):
        self.sBox = c.sBox
        self.s_box_inverted = c.sBoxInverted
        self.round_const = c.roundConst
        self.key_schedule = []

    def encrypt(self, source, key):
        self.key_expansion(key)

        encrypted = []
        blocks = self.make_blocks(source)

        for block in blocks:
            encrypted.append(self.encryptBlock(block))
        
        encrypted_text = ''
        for block in encrypted:
            encrypted_text+= decode_block(block)
        return encrypted_text  

    def decrypt(self, cipher, key):
        decrypted = []
        blocks = self.make_blocks(cipher)

        for block in blocks:
            decrypted.append(self.decryptBlock(block))
        
        decrypted_text = ''
        for block in decrypted:
            decrypted_text+= decode_block(block)
        return decrypted_text  

    def encryptBlock(self, block):
        key_schedule = self.key_schedule
        state = [[None for _ in range(4)]for _ in range(4)]

        for r in range(4):
            for c in range(4):
                state[r][c] = block[r + 4*c]
        state = self.addRoundKey(state, key_schedule[0])

        for i in range(1,10):
            state = self.subBytes(state)
            state = self.shiftRows(state)
            state = self.mixColumns(state)
            state = self.addRoundKey(state, key_schedule[i])

        state = self.subBytes(state)
        state = self.shiftRows(state)
        state = self.addRoundKey(state, key_schedule[-1])

        return state

    def decryptBlock(self, block):
        key_schedule = self.key_schedule
        state = [[None for _ in range(4)]for _ in range(4)]

        for r in range(4):
            for c in range(4):
                state[r][c] = block[r + 4*c]
        state = self.addRoundKey(state, key_schedule[0])

        for i in range(1,10):
            state = self.reverseSubBytes(state)
            state = self.reverseShiftRows(state)
            state = self.reverseMixColumns(state)
            state = self.addRoundKey(state, key_schedule[i])

        state = self.reverseSubBytes(state)
        state = self.reverseShiftRows(state)
        state = self.addRoundKey(state, key_schedule[-1])

        return state

    def key_expansion(self, key):
        keys = key
        if len(keys) < 16:
            while len(keys)!= 16:
                keys += ' '
        

        key_schedule = self.split(self.make_blocks(keys)[0], 4)

        for i in range(4,44):
            if i % 4 == 0:
                prev = key_schedule[i-1]
                current_row = self.swapBytes(self.shift(prev,-1))
                prev_row = key_schedule[i-4]
                const = c.roundConst[int(i/4)-1]
                key_schedule.append(self.XOR(current_row,prev_row, const))
            else:
               key_schedule.append(self.XOR(key_schedule[-1], key_schedule[i-4])) 
                
        self.key_schedule = self.split(key_schedule, 4)
  
    def addRoundKey(self, state, round_key):
        result = [[None for _ in range(4)]for x in range(4)]
        for i in range(4):
            for j in range(4):
                result[i][j] = round_key[i][j] ^ state[i][j]
        return result

    def mixColumns(self, state):
        for i in range(4):
            s0 = x_02(state[0][i]) ^ x_03(state[1][i]) ^ state[2][i] ^ state[3][i]
            s1 = state[0][i] ^ x_02(state[1][i]) ^ x_03(state[2][i]) ^ state[3][i]
            s2 = state[0][i] ^ state[1][i] ^ x_02(state[2][i]) ^ x_03(state[3][i])
            s3 = x_03(state[0][i]) ^ state[1][i] ^ state[2][i] ^ x_02(state[3][i])

            state[0][i] = s0
            state[1][i] = s1
            state[2][i] = s2
            state[3][i] = s3

        return state

    def reverseMixColumns(self, state):
        for i in range(4):
            s0 = x_0e(state[0][i]) ^ x_0b(state[1][i]) ^ x_0d(state[2][i]) ^ x_09(state[3][i])
            s1 = x_09(state[0][i]) ^ x_0e(state[1][i]) ^ x_0b(state[2][i]) ^ x_0d(state[3][i])
            s2 = x_0d(state[0][i]) ^ x_09(state[1][i]) ^ x_0e(state[2][i]) ^ x_0b(state[3][i])
            s3 = x_0b(state[0][i]) ^ x_0d(state[1][i]) ^ x_09(state[2][i]) ^ x_0e(state[3][i])

            state[0][i] = s0
            state[1][i] = s1
            state[2][i] = s2
            state[3][i] = s3

        return state

    def shiftRows(self, block):
        rows = block
        shifted_rows = []
        for i in range(4):
            shifted_row = self.shift(rows[i], i)
            shifted_rows.append(shifted_row)
        return shifted_rows

    def reverseShiftRows(self, block):
        rows = block
        shifted = []
        for i in range(4):
            shifted_row = self.shift(rows[i], -i)
            shifted.append(shifted_row)
        return shifted

    def subBytes(self, state):
        for i in range(4):
            for j in range(4):
                value = hex(state[i][j])
                if len(value)<4:
                    x = 0
                    y = int(hex(state[i][j])[-1], 16)
                else:    
                    x = int(hex(state[i][j])[-1], 16)
                    y = int(hex(state[i][j])[-2], 16)
                state[i][j] = c.sBox[x][y]
        return state

    def swapBytes(self, list):
        for i in range(len(list)):
            value = hex(list[i])
            if len(value) < 4:
                x = 0
                y = int(hex(list[i])[-1], 16)    
            else:
                x = int(hex(list[i])[-1], 16)
                y = int(hex(list[i])[-2], 16)
            list[i] = c.sBox[x][y]
        return list    

    def reverseSubBytes(self, state):
        for i in range(4):
            for j in range(4):
                value = hex(state[i][j])    
                
                if len(value)<4:
                    x = 0
                    y = int(hex(state[i][j])[-1], 16)
                else:    
                    x = int(hex(state[i][j])[-1], 16)
                    y = int(hex(state[i][j])[-2], 16)
                
                state[i][j] = c.sBoxInverted[x][y]
        return state

    def make_blocks(self, source):
        blocks = self.split(source, 16)
        length = len(blocks)

        for block in blocks:
            if len(block) < 16:
                for _ in range(16 - length):
                    block.append(0x1)

            for i in range(len(block)):
                if type(block[i]) is str:
                    block[i] = ord(block[i])

        return blocks

    def split(self, source, number):
        result = []
        for i in range(0, len(source), number):
            result.append(list(source[i:i+number]))
        return result

    def shift(self, row, number):
        temp = []
        length = len(row)
        x = number
        for i in range(len(row)):
            temp.append(row[(i-number) % length])
        return temp

    def XOR(self,*args):
        result = []
        length = len(args[0])

        for i in range(length):
            temp = args[0][i]
            for j in range(1, len(args)):
                temp = args[j][i]^temp   
            result.append(temp)
        return result    

def print_block(block):
    for row in block:
        print(row)

def decode_block(block):
    decoded = ''
    for i in range(4):
        for j in range(4):
            decoded+=chr(block[i][j])
    return decoded        

def test():

    str_test = 'string for testing american encryption standart cipher'
    key_test = 'cipherkey'


    aes = AES()
    
    encrypted = aes.encrypt(str_test,key_test)
    decrypted = aes.decrypt(encrypted,key_test)
    decrypted = str_test
    print('encrypted: ') 
    print(encrypted)
    print()
    print('decrypted: ') 
    print(decrypted)

def main():
    test()        

main()
