# This is an implementation of 1-2 Oblivious transfer
# Oblivious transfer is an interactive protocol. 
# Coroutines using yield is used to model communication between 2 parties alice and bob

from random import getrandbits
from gen_rsa_params import gen_rsa_params

def oblivious_transfer_alice(m0, m1, e, d, N, nbits = 2048):
    x0, x1 = getrandbits(nbits), getrandbits(nbits)
    v = yield(x0, x1, e, N)
    k0 = pow(v-x0, d, N)
    k1 = pow(v-x1, d, N)
    m0k = (m0 + k0) % N
    m1k = (m1 + k1) % N
    yield m0k, m1k

def oblivious_transfer_bob(b, nbits = 2048):
    assert b in (0, 1)
    x0, x1, e, N = yield
    k = getrandbits(nbits)
    v = ((x0, x1)[b] + pow(k, e, N)) % N
    m0k, m1k = yield v
    mb = ((m0k, m1k)[b] - k) % N
    yield mb

def oblivious_transfer(alice, bob):
    x0, x1, e, N = next(alice)
    next(bob)
    v = bob.send((x0, x1, e, N))
    m0k, m1k = alice.send(v)
    mb = bob.send((m0k, m1k))
    return mb
