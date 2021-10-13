def bytes_to_bits(inp) -> list:
    res = []
    for v in inp:
        res += list(map(int, format(v, '08b')))
    return res

def bits_to_bytes(inp):
    res = []
    for i in range(0, len(inp), 8):
        res.append(int(''.join(map(str, inp[i: i + 8])), 2))
    return bytes(res)

def xor(a, b):
    return [x ^ y for x, y in zip(a, b)]