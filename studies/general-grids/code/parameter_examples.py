"""Validate the two parameter-only large examples without constructing a quadratic direction table."""
from anchor_ring import prime,chi,finite_rays,high_odd_tests
p,k=250057,5445
assert prime(p) and p%24==1 and chi(k,p)==-1 and finite_rays(p,k)
for d,H in high_odd_tests(p):
 rhs=k*pow(d,-1,p)%p;r=next(z for z in range(1,p//2+1)if z*z%p==rhs);assert H*r<(H-4)*p
assert (4*p+1,6*p+2)==(1000229,1500344)
print('PASS p=250057 k=5445: all least-root inequalities and boundary-ray certificate; n=1000229, points=1500344.')
p=660241;lo=1320437;hi=1320533
assert prime(p) and p%840==1 and prime(lo) and prime(hi) and lo<2*p<hi and not any(prime(i)for i in range(lo+1,hi))
assert 4*p+1==2640965 and 2*hi-1==2641065 and 2*hi-(4*p+1)==101 and 6*p+2-3*(lo-1)==140
print('PASS p=660241: every one of 101 consecutive sides gains 140 relative to the largest-prime HJSW embedding; not 140 over 3n/2.')
