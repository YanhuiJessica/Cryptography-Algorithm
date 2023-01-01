from tables import *
from utils import *

def block_encrypt(plaintext: bytes, key: bytes) -> bytes:
    # check length
    assert len(plaintext) == 16
    assert len(key) in [16, 24, 32]

    n_rounds = len(key) // 4 + 6
    round_keys = expand_key(key, n_rounds)
    state = bytes2matrix(plaintext)

    state = add_round_key(state, round_keys[0])

    for i in range(1, n_rounds):
        state = sub_bytes(state, S_BOX)
        shift_rows(state)
        mix_columns(state)
        state = add_round_key(state, round_keys[i])

    # Final round
    state = sub_bytes(state, S_BOX)
    shift_rows(state)
    state = add_round_key(state, round_keys[n_rounds])

    return matrix2bytes(state)

def block_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    # check length
    assert len(ciphertext) == 16
    assert len(key) in [16, 24, 32]

    n_rounds = len(key) // 4 + 6
    round_keys = expand_key(key, n_rounds)
    state = bytes2matrix(ciphertext)

    state = add_round_key(state, round_keys[n_rounds])

    for i in range(n_rounds - 1, 0, -1):
        inv_shift_rows(state)
        state = sub_bytes(state, INV_S_BOX)
        state = add_round_key(state, round_keys[i])
        inv_mix_columns(state)

    # Final round
    inv_shift_rows(state)
    state = sub_bytes(state, INV_S_BOX)
    state = add_round_key(state, round_keys[0])

    return matrix2bytes(state)