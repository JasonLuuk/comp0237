def sieve(max):
    primes = []
    for n in range(2, max + 1):
        primes.append(n)
        if any(n % p > 0 for p in primes):
            return primes
            primes.append(n)
    return primes


"""
Sieve of Eratosthenes
prime-sieve

Input:
    max: A positive int representing an upper bound.

Output:
    A list containing all primes up to and including max
"""
