import os, sys

sys.path.append(os.path.join(sys.path[0], '..'))

from tables import *
from general import *

def initital_permutation_IP(bits: list):
    res = []
    for i in IPtable:
        res.append(bits[i - 1])  # 数组下标从 0 开始
    return res

def final_permutation_re_IP(bits: list):
    res = []
    for i in rIPtable:
        res.append(bits[i - 1])
    return res

def permutation_choose(keybits: list, num: int):
    permuted = []
    for i in (PC_1 if num == 1 else PC_2):
        permuted.append(keybits[i - 1])
    return permuted

def extend_permutation(bits: list):
    res = []
    for i in E:
        res.append(bits[i - 1])
    return res

def permutation(bits: list):
    res = []
    for i in P:
        res.append(bits[i - 1])
    return res

def substitution(bits: list):
    res = []
    for i in range(8):
        m = bits[i * 6: i * 6 + 6]
        row = int(f'{m[0]}{m[5]}', 2)
        col = int(f'{m[1]}{m[2]}{m[3]}{m[4]}', 2)
        res.extend(list(map(int, format(S[i][row * 16 + col], '04b'))))  # 转化成 4 位二进制数
    return res

def rotate_left(bits: list, cnt: int):
    res = bits[cnt:]
    res += bits[:cnt]
    return res

def keygen(keybits: list):
    permuted = permutation_choose(keybits, 1)
    key_C0 = permuted[:28]
    key_D0 = permuted[28:]

    keys = []

    for i in SHIFT:
        key_c = rotate_left(key_C0, i)
        key_d = rotate_left(key_D0, i)
        keys.append(permutation_choose(key_c + key_d, 2))

    return keys

def f(bits: list, key: list):
    return permutation(substitution(xor(extend_permutation(bits), key)))

def block_encrypt(plainbits: list, keybits: list):
    # check length
    assert len(plainbits) == 64
    assert len(keybits) == 64

    permuted = initital_permutation_IP(plainbits)
    permuted_left = permuted[:32]
    permuted_right = permuted[32:]
    keys = keygen(keybits)

    for i in range(15):
        pre_right = permuted_right
        permuted_right = xor(f(permuted_right, keys[i]), permuted_left)
        permuted_left = pre_right

    # Do not need to reverse in round 16
    permuted_left = xor(f(permuted_right, keys[15]), permuted_left)

    return final_permutation_re_IP(permuted_left + permuted_right)

def block_decrypt(cipherbits: list, keybits: list):
    # check length
    assert len(cipherbits) == 64
    assert len(keybits) == 64

    permuted = initital_permutation_IP(cipherbits)
    permuted_left = permuted[:32]
    permuted_right = permuted[32:]
    keys = keygen(keybits)

    for i in range(15, 0, -1):
        pre_right = permuted_right
        permuted_right = xor(f(permuted_right, keys[i]), permuted_left)
        permuted_left = pre_right

    permuted_left = xor(f(permuted_right, keys[0]), permuted_left)

    return final_permutation_re_IP(permuted_left + permuted_right)