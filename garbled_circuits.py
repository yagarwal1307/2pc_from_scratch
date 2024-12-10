import itertools
import functools
import operator
from random import getrandbits

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Hash import SHA3_256
from Crypto.Random.random import shuffle

def symmetric_enc(key, x):
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(pad(long_to_bytes(x), 16))
    nonce = cipher.nonce
    return ciphertext, tag, nonce

def symmetric_dec(key, nonce, ciphertext, tag):
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    x = bytes_to_long(unpad(cipher.decrypt_and_verify(ciphertext, tag), 16))
    return x

def combine_keys(keys):
    h = SHA3_256.new()
    for key in keys:
        h.update(long_to_bytes(key))
    return h.digest()

def label_table(logic_table, output_name, input_names, k=128):
    labels = {}
    for var in (output_name, *input_names):
        # TODO: this is wrong. Both the labels should be unique. there is a chance of overlap in this implementation
        labels[var] = [getrandbits(k), getrandbits(k)]

    labeled_table = []
    for inp_values in itertools.product((0,1), repeat=len(input_names)):
        output_value = functools.reduce(operator.getitem, inp_values, logic_table)
        output_label = labels[output_name][output_value]
        input_labels = [labels[input_names[i]][v] for i,v in enumerate(inp_values)]
        labeled_table.append((output_label, input_labels))

    return labeled_table, labels

def garble_table(labeled_table, k=128):
    result = []
    for row in labeled_table:
        output_label, input_labels = row
        key = combine_keys(input_labels)
        c, tag, nonce = symmetric_enc(key, output_label)
        result.append((c, tag, nonce))
    shuffle(result)
    return result

def eval_garbeled_table(garbled_table, inputs):
    for row in garbled_table:
        ciphertext, tag, nonce = row
        try:
            key = combine_keys(inputs)
            output_label = symmetric_dec(key, nonce, ciphertext, tag)
        except ValueError:
            continue
        return output_label
