IP = (2, 6, 3, 1, 4, 8, 5, 7)
E = (4, 1, 2, 3, 2, 3, 4, 1)
IP_INVERSE = [4, 1, 3, 5, 7, 2, 8, 6]
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
P4 = [2, 4, 3, 1]

S0 = [[1, 0, 3, 2],
      [3, 2, 1, 0],
      [0, 2, 1, 3],
      [3, 1, 3, 2]]

S1 = [[0, 1, 2, 3],
      [2, 0, 1, 3],
      [3, 0, 1, 0],
      [2, 1, 0, 3]]


def permutate(original, fixed_key):
    return ''.join(original[i - 1] for i in fixed_key)


def left_half(bits):
    return bits[:len(bits)//2]


def right_half(bits):
    return bits[len(bits)//2:]


def shift(bits):
    rotated_left_half = left_half(bits)[1:] + left_half(bits)[0]
    rotated_right_half = right_half(bits)[1:] + right_half(bits)[0]
    return rotated_left_half + rotated_right_half


def key1(KEY):
    return permutate(shift(permutate(KEY, P10)), P8)


def key2(KEY):
    return permutate(shift(shift(shift(permutate(KEY, P10)))), P8)


def xor(bits, key):
    return ''.join(str(((bit + key_bit) % 2)) for bit, key_bit in
                   zip(map(int, bits), map(int, key)))


def lookup_in_sbox(bits, sbox):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    return '{0:02b}'.format(sbox[row][col])


def f_k(bits, key):
    L = left_half(bits)
    R = right_half(bits)
    bits = permutate(R, E)
    bits = xor(bits, key)
    bits = lookup_in_sbox(left_half(bits), S0) + lookup_in_sbox(right_half(bits), S1)
    bits = permutate(bits, P4)
    return xor(bits, L)


def decrypt(cipher_text,KEY):
    bits = permutate(cipher_text, IP)
    temp = f_k(bits, key2(KEY))
    bits = right_half(bits) + temp
    bits = f_k(bits, key1(KEY))
    return permutate(bits + temp, IP_INVERSE)

Cipher_list = [0b111110,0b1010001,0b1101110,0b11110101,0b10111111,0b1101110,0b11110101,0b11110101,0b11000101,0b10111111,0b1010001,0b10110,0b10111111,0b111110,0b11110101,0b11001011,0b10110100,0b1010011,0b11000101,0b111110,0b111110,0b10110100,0b10110100,0b10110100,0b11110101,0b11001011,0b1101110,0b11001011,0b111110,0b10111111,0b11000101,0b10111111,0b10110100,0b1010011,0b11001011,0b1010011,0b11110101,0b10110100,0b11000101,0b11110101,0b1010011,0b10111111,0b11110101,0b10110,0b11000101,0b10110100,0b11001011,0b1010011,0b10110,0b10110100,0b1010011,0b10111111,0b10110,0b1010001,0b111110,0b1010011,0b1101110,0b1010001,0b11000101,0b10110,0b11001011,0b10110,0b111110,0b11001011,0b11000101,0b10110,0b11110101,0b11000101,0b11001011,0b1010001,0b10111111,0b11000101,0b11000101,0b10110,0b11001011,0b111110,0b1010001]
ID = "590610668"
Check_list = ID.encode('utf8')

for i in range (1024):
    count_check = 0
    
    print("\n \n -------------KEY------------------" + str('{0:010b}'.format(i)))

    for j in range (len(Cipher_list)):
        KEY = str('{0:010b}'.format(i))
        Cipher = str('{0:08b}'.format(Cipher_list[j]))
        plain = int(decrypt(Cipher,KEY),2)
        
        if j <= 8 :
            if plain != int(Check_list[j]):
                break
            else:
                count_check += 1
        print (str(plain - 48) + ",", end = '')
            
    if count_check >= 9:
        break
