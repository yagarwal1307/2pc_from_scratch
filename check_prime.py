from random import randrange

# We can optimise this method using sieve of erestostheuns for small primes
def check_prime(n, k=40) -> bool:
    "It's a rabin miller primality test implementation"
    if (n == 2):
        return True
    if (n%2 == 0):
        return False
    
    # Assuming n-1 = 2**s * r
    r, s = n-1, 0
    while (r%2 == 0):
        s += 1
        r //= 2

    for _ in range(k):
        a = randrange(2, n-2)
        x = pow(a, r, n)
        if (x == 1 or x == n-1):
            continue
        
        for _ in range(s-1):
            x = pow(x, 2, n)
            if (x == n-1):
                break
        
        if (x != n-1):
            return False
        
    return True
        
def gen_small_primes(n=20000):
    sieve = [True]*(n+1)
    sieve[0] = sieve[1] = False
    for start in range(2, int(n ** 0.5) + 1):
        if sieve[start]:
            for multiple in range(start*start, n+1, start):
                sieve[multiple] = False
    return [num for num, is_prime in enumerate(sieve) if is_prime]

SMALL_PRIMES = gen_small_primes()

def is_divisible_by_small_primes(n) -> bool:
    for p in SMALL_PRIMES:
        if (n%p == 0):
            return True
    return False
