def KSA(key: bytes) -> list:
    '''
    Key-scheduling algorithm
    '''
    key_length = len(key)
    S = list(range(256)) # 0~255 填充 S 数组

    # 依据提供的密钥置换
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i] # swap

    return S

def PRGA(S):
    '''
    Pseudo-random generation algorithm

    加密的同时继续置换数组 S
    '''
    i, j = 0, 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        k = S[(S[i] + S[j]) % 256]
        yield k # 返回生成器，当调用函数时并不运行函数体内的代码，每次调用 __next__() 执行一次循环体

def encrypt(key: str, plaintext: str, hexstr: bool = False) -> str:
    '''
    `key` - 用于加密的密钥

    `plaintext` - 需要加密的明文

    `hexstr` - 标记明文是否是十六进制字符串

    返回密文十六进制字符串
    '''
    # 将字符转换为字节
    key = key.encode('utf-8')
    # 依据明文类型采用不同方式
    if hexstr: plain = bytes.fromhex(plaintext)
    else: plain = plaintext.encode('utf-8')

    keystream = PRGA(KSA(key))  # 取得密钥流

    cipher = []
    for c in plain:
        val = '%02x' % (c ^ keystream.__next__())  # 异或并转化为 hex 值
        cipher.append(val)

    print('\nEncrypted data:')
    print_result(''.join(cipher))

    return ''.join(cipher)

def decrypt(key: str, ciphertext: str, hexstr: bool = False) -> str:
    '''
    `key` - 用于解密的密钥

    `ciphertext` - 需要解密的密文

    `hexstr` - 标记密文是否是十六进制字符串

    返回明文十六进制字符串
    '''
    # 将字符转化为字节
    key = key.encode('utf-8')
    # 依据密文类型采用不同方式
    if hexstr: cipher = bytes.fromhex(ciphertext)
    else: cipher = ciphertext.encode('utf-8')

    keystream = PRGA(KSA(key))  # 取得密钥流

    plain = []
    for c in cipher:
        val = '%02x' % (c ^ keystream.__next__())  # 异或并转化为 hex 值
        plain.append(val)

    print('\nDecrypted data:')
    print_result(''.join(plain))

    return ''.join(plain)

def print_result(text: str) -> None:
    print('HEX: 0x' + text)
    try:
        print('STR:', bytes.fromhex(text).decode('utf-8'))  # 尝试使用 UTF-8 解码
    except:
        print('STR:', bytes.fromhex(text))

if __name__ == '__main__':
    key = input('Key: ')
    plain = input('Plain text: ')

    cipher = encrypt(key, plain)

    decrypt(key, cipher, True)