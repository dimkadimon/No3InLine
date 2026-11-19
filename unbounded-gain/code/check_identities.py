#!/usr/bin/env python3
"""Small-field checks on the algebra in the proof; not an asymptotic argument."""
from collections import defaultdict
from itertools import combinations
from random import Random
from math import gcd
from fractions import Fraction


def audit(p):
    inv = [0] + [pow(a, -1, p) for a in range(1, p)]
    templates = defaultdict(list)
    hit = same = cross = exceptional = 0
    rng = Random(11223 + p)
    for k in range(1, p):
        for x in range(p):
            for y in range(p):
                if (x*y-k) % p == 0:
                    continue
                lines = defaultdict(list)
                for U in range(1, p):
                    V = k * inv[U] % p
                    if U != x and V != y:
                        lines[(V-y)*inv[(U-x) % p] % p].append((U,V))
                chords = []
                for slope, pts in lines.items():
                    if len(pts) != 2:
                        assert len(pts) == 1
                        continue
                    (U,V), (W,Z) = pts
                    a = U; b = a*slope % p
                    t, u = (U-x)*inv[a] % p, (W-x)*inv[a] % p
                    assert (V-y-b*t) % p == (Z-y-b*u) % p == 0
                    assert (k-x*y+a*b*t*u) % p == (b*x+a*y+a*b*(t+u)) % p == 0
                    # The ratio equation, with r=t and s=u, also covers t=-u.
                    assert ((u*(y*U-x*V))**2-(k-x*y)*((t+u)**2*k-(t-u)**2*x*y)) % p == 0
                    chords.append((a,b,t,u,U,W));hit += 1
                    templates[k].append((a,b,t,u,U))
                for g, gg in combinations(chords, 2):
                    a,b,t,u,U,W = g; A,B,T,S,Q,R = gg
                    for t0,u0,v0 in [(t,u,U),(u,t,W)]:
                        for t1,u1,v1 in [(T,S,Q),(S,T,R)]:
                            e=v1*inv[v0] % p
                            alpha,beta=A*inv[a] % p,B*inv[b] % p
                            c,d=u0*inv[t1] % p,t0*inv[u1] % p
                            assert e != 1 and (alpha*beta-c*d) % p == (alpha-e*beta-(1-e)*c) % p == 0
                            same += 1
        # Two-root identity at one level; identity itself does not require roots to be distinct.
        pool = templates[k]
        for _ in range(3500):
            a,b,t,u,U = rng.choice(pool); A,B,T,S,V = rng.choice(pool)
            e = V*inv[U] % p
            ell = (b*inv[a]-e*e*B*inv[A]) % p
            rr = (e*B*(S-T)-b*(u-t)) % p
            assert (ell*U-rr) % p == 0
            if ell == rr == 0:
                assert (a*b*(u-t)**2-A*B*(S-T)**2) % p == 0
                assert e == b*(u-t)*inv[B*(S-T)%p] % p
                exceptional += 1
            cross += 1
    print(f'p={p}: hits={hit}, same-root ordered endpoint comparisons={same}, two-root samples={cross}, exceptional={exceptional}: PASS')


def main():
    slopes = {(a,b) for a in range(1,9) for b in range(-8,9) if b and gcd(a,b) == 1}
    beta = {Fraction(r-s,r+s)**2 for r in range(-8,9) for s in range(-8,9) if r*s and r not in {s,-s}}
    assert len(slopes)==86 and len(beta)==42 and not ({0,1} & beta)
    print('One-root level sieve: 86 primitive slopes, 42 reduced ratio shifts, plus 0 and xy = 130 distinct formal shifts: PASS')
    for p in (11,13,17):
        audit(p)
    # Distinct ordinary templates with identical modular offsets and neither height short.
    p=101; M=((-110,10),(-99,9)); Z=((-9,10),(-99,110))
    det = lambda A: A[0][0]*A[1][1]-A[0][1]*A[1][0]
    E=tuple(tuple((Z[i][j]-M[i][j])//p for j in range(2)) for i in range(2))
    assert det(M)==det(Z)==0 and E==((1,0),(0,1))
    assert all((Z[i][j]-M[i][j])%p==0 for i in range(2) for j in range(2))
    print('Rank-two lift difference: M=(10,9)^T(-11,1), M\'=(1,11)^T(-9,10); M\'-M=101 Id: PASS')

if __name__ == '__main__':
    main()
