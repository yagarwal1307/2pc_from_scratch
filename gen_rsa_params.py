from random import getrandbits
from check_prime import check_prime, is_divisible_by_small_primes

def gen_prime(nbits=2048):
    while True:
        n = getrandbits(nbits)
        n |= 1

        if is_divisible_by_small_primes(n):
            continue

        if check_prime(n):
            return n

def gen_rsa_params(nbits=2048):
    p, q = gen_prime(nbits), gen_prime(nbits)
    N = p * q
    e = 65537
    phi = (p-1)*(q-1)
    d = pow(e, -1, phi)
    return e, d, N

    