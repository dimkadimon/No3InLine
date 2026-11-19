#!/usr/bin/env python3
"""Check the finite scale examples in Appendix A, offline (Python 3.9+).
This verifies arithmetic, not the probabilistic estimates or an infinite cap family.
The three candidate factors of Phi_840(3) were located via FactorDB, entry
1100000000498735166. Their primality and completeness are proved below
without using a factor database, a probable-prime oracle, or a CAS at replay time.
"""
from decimal import Decimal, localcontext
from functools import lru_cache
from itertools import product
from math import gcd, isqrt, prod
from pathlib import Path
import hashlib
import json
import zipfile

if not __debug__:
    raise SystemExit('Run without Python -O; checks use assertions.')

FACTORS = (162410641, 120269035510423913774671677928007008342081,
           2047314589905164660182861222233071665633201)
# n: (Lucas witness, full factorization of n-1); leaves proved by trial division.
CERT = {
    162410641: (11, {2: 4, 3: 1, 5: 1, 7: 1, 277: 1, 349: 1}),
    20652868853: (5, {2: 2, 7: 1, 11: 1, 1871: 1, 35839: 1}),
    3345764754187: (2, {2: 1, 3: 4, 20652868853: 1}),
    53532236066993: (3, {2: 4, 3345764754187: 1}),
    698265251: (6, {2: 1, 5: 3, 409: 1, 6829: 1}),
    63849374551441: (7, {2: 4, 3: 2, 5: 1, 127: 1, 698265251: 1}),
    120269035510423913774671677928007008342081: (46, {2: 6, 3: 1, 5: 1, 7: 1, 11: 1, 13: 1, 1601: 1, 22871: 1, 53532236066993: 1, 63849374551441: 1}),
    1113491: (7, {2: 1, 5: 1, 7: 1, 15907: 1}),
    8907929: (3, {2: 3, 1113491: 1}),
    17815859: (2, {2: 1, 8907929: 1}),
    35631719: (7, {2: 1, 17815859: 1}),
    13399087882897: (5, {2: 4, 3: 2, 222601: 1, 418009: 1}),
    510497106627155761: (23, {2: 4, 3: 2, 5: 1, 7: 1, 17: 1, 419: 1, 55631: 1, 255613: 1}),
    2047314589905164660182861222233071665633201: (11, {2: 4, 3: 1, 5: 2, 7: 1, 35631719: 1, 13399087882897: 1, 510497106627155761: 1}),
}


def trial_prime(n):
    return n >= 2 and all(n % k for k in range(2, isqrt(n) + 1))


@lru_cache(None)
def prove_prime(n):
    if n < 10**6:
        assert trial_prime(n), n
        return
    a, powers = CERT[n]
    assert all(2 <= q < n and e > 0 for q, e in powers.items())
    assert prod(q**e for q, e in powers.items()) == n - 1
    for q in powers:
        prove_prime(q)
    assert pow(a, n-1, n) == 1
    assert all(gcd(pow(a, (n-1)//q, n)-1, n) == 1 for q in powers)
    # Modulo every prime r | n, a has order n-1. Thus r >= n and n is prime.


@lru_cache(None)
def phi3(j):
    others = prod(phi3(d) for d in range(1, j) if j % d == 0)
    q, rem = divmod(3**j - 1, others)
    assert rem == 0
    return q


def verify_order(p, d):
    assert pow(3, d, p) == 1
    assert all(pow(3, d//q, p) != 1 for q in range(2, d+1) if d % q == 0 and trial_prime(q))


def check():
    dets = [a*d-b*c for a,b,c,d in product(range(-8, 9), repeat=4)]
    assert (len(dets), sum(bool(v) for v in dets), max(map(abs, dets))) == (83521, 81152, 128)
    print('Matrix box: 83,521 total; 81,152 nonsingular over Q; maximum |det| = 128.')
    assert phi3(840) == prod(FACTORS) and list(FACTORS) == sorted(FACTORS)
    for f in FACTORS:
        prove_prime(f)
        verify_order(f, 840)
    print('Phi_840(3) =', phi3(840))
    print('Certified complete factorization:', ' * '.join(map(str, FACTORS)))
    print('Each prime factor has ord_p(3) = 840.')
    primes = [p for p in range(1, 4202, 840) if trial_prime(p)]
    assert primes == [2521, 3361, 4201]
    kit = Path(__file__).with_name('no3-replay-r2.zip')
    assert hashlib.sha256(kit.read_bytes()).hexdigest() == '238f38e60234b982cd0ba13045bfad4809fb00e764d0eb1278bfeb7378d6d9ca'
    with zipfile.ZipFile(kit) as z:
        points = {row['p']: row for row in json.loads(z.read('small-prime-examples/examples.json'))}
        p0, _, pairs0, _ = map(int, z.read('unbounded-gain/data/certificate.txt').splitlines()[0].split())
        assert (p0, pairs0) == (797161, 2)
    print('p | ord | index I | J/L^3 | N | I >= L^24 | directly certified pairs')
    for p, d in [(2521, 126), (3361, 1680), (4201, 420), (797161, 13), *((f, 840) for f in FACTORS)]:
        prove_prime(p)
        verify_order(p, d)
        h = d if d % 2 == 0 else 2*d
        assert p % 840 == 1 and (p-1) % h == 0
        I = (p-1)//h
        with localcontext() as ctx:
            ctx.prec = 70
            L = 1 + Decimal(p).ln()
            J = min(Decimal(I), Decimal(p).sqrt())
            scale = J/L**3
            assert I < L**24
            if p in primes:
                row = points[p]
                pairs = len(row['representatives'])
                assert row['points'] == 6*(p-1) + 8 + 2*pairs
                assert (int(scale), pairs) == (0, {2521:118, 3361:146, 4201:150}[p])
            elif p == p0:
                pairs = pairs0
                assert int(scale) == 0
            else:
                pairs = 'not computed'
            if p == FACTORS[0]:
                assert int(scale) == 1
            print(f'{p} | {d} | {I} | {scale:.7g} | {int(scale)} | no | {pairs}')
            if p == FACTORS[-1]:
                print(f'Largest factor: I = {Decimal(I):.3E}; L^24 = {L**24:.3E}.')
    print('PASS exact matrix and cyclotomic arithmetic, prime and order certificates, finite scale comparison.')


if __name__ == '__main__':
    check()
