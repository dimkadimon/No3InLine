# Eight boundary points beyond the four-period ring

**Result.** For every prime `p = 1 (mod 24)`, the ordinary integer square of side `n=4p+1` contains a set of `6p+2 = ceil(3n/2)` points, invariant under the half-turn about the board centre. This is an **infinite additive gain of 1/2 over 3n/2**, not an improved leading coefficient. There is also an explicit half-turn construction for `3p <= n <= 4p` at every prime `p>3`, with at least `2n-2p-42` points (`2n-2p-6` for `p=1 mod 12`). Together with the prime number theorem and the small-board fallback this provides a family indexed by every `n`, of size at least `(3/2-o(1))n`. It is not a claim of world-record finite scores, a new unrestricted leading asymptotic, or a single infinite set with these restrictions.

Read **boundary-rings.pdf** for the proofs. `boundary-rings.tex` is its source; `ring-figure.pdf` plots actual coordinates and the edit obstruction. Offline reproductions of the main results need only Python 3.9+; a C++17 compiler is used for the independent quadratic-time example checks. No solver is required for the theorems or generator.

## Produce coordinates

From this directory:

```sh
python3 code/anchor_ring.py --n 10000 --csv set.csv
python3 code/anchor_ring.py --p 73 --csv set293.csv
python3 code/anchor_ring.py --p 1009
python3 code/anchor_ring.py --ordinary --n 294 --csv ordinary294.csv
```

`--n` takes **any** positive side and always uses the board's own centre; it tries a nearby unrestricted prime on either side of `n/4`, nearby `1 mod 12` primes, and an embedded anchored set for odd `n`. For modest `n` with no effective ring it falls back to centred modular circles or the corners. This is a lower-bound algorithm, not an optimiser. `--ordinary --n N` additionally compares with the half-turn construction of side `N-1` when `N` is even and with the classical prime embedding of size `H(N)=3(P(N/2)-1)`, where `P` is the preceding prime. It never underperforms `H(N)` for `N>=6`; its output need not preserve the board half-turn. `--p` produces the explicit anchored special family; an input prime congruent to 1 modulo 24 is required. Output is a zero-based CSV `x,y`. For the rectangular construction directly without choosing the prime, import `rect(n,p)` from `code/anchor_ring.py`; it returns `(level, list_of_points)`.

## Checks and certificates

```sh
python3 code/check_certificates.py  # independent proof checker: no import from generator
python3 code/prime_audit.py         # recreate and compare all entries to the stored table
python3 code/test_family.py         # 288 rectangular cases, 121 all-size inputs, edit-count checks
c++ -O3 -std=c++17 code/all_lines.cpp -o all_lines
./all_lines 293 data/n293.csv 440
./all_lines 389 data/n389.csv 584
./all_lines 4037 data/n4037.csv 6056
./all_lines 10085 data/n10085.csv 15128
./all_lines 294 ordinary294.csv 440 --ordinary  # if generated above
python3 code/parameter_examples.py
sha256sum -c SHA256SUMS
```

The C++ checker does not import the modular construction, assume its slope restrictions or use a floating-point tolerance. At every anchor it checks for duplicate unoriented primitive integer directions, as well as checking the count, coordinate bounds and half-turn invariance. `data/geometry-audit.txt` gives its output. `data/general-examples.txt` checks four arbitrary-side outputs. This full coordinate audit is quadratic (plus sorting) and is not necessary to certify examples with millions of points: use the theorem instead. The million-wide example in the PDF has `p=250057, k=5445`, `n=1000229`, `1500344` points; it was checked by its prime and exact ray/level conditions, not by a quadratic scan.

`data/prime-certificates.csv` contains exactly the 194 primes `p<=B(p)` that the box proof does not settle directly; `B(p)<=50625`. In 191 rows the level alone certifies the required least-root bounds. In the three other rows the independent code reconstructs the old points from the defining congruence and scans directions from **all twelve** candidate noncorner boundary sites. The 81 eight-anchor choices (9 half-turn invariant) are compatible at each stated level. For `p=1 mod 840`, no tuning or finite enumeration is needed: for every nonsquare level all low-height anchor-ray products are squares. A separate checker confirms the interior midpoint counts in the note.

## Comparison against just rounding down to a prime

Corollary C of the note gives infinitely many intervals of length at least `c log N` on which the anchored construction exceeds `H(n)` by at least `c log N` throughout. Its proof uses the Chinese remainder theorem and Linnik’s least-prime theorem. This is *not* logarithmic excess over `3n/2`: it exploits prime gaps at the `n/2` benchmark and the available prime at a different scale. For example, at `p=660241` the same `3961448` points beat the embedding benchmark by `140` for 101 consecutive sides (`2640965` through `2641065`).

## Search for a linear rather than additive gain

These are explicitly **restricted** tests. They are neither needed for the proved results nor certificates of an unrestricted upper bound.

* `code/rect_probe.py`, `data/rect-probe.txt`: in six primes, tried exhaustive improvements inside individually shortened rectangular fibres with the rest of a particular seed fixed. None of the recorded trials gained a point. `code/cluster_probe.py`, `data/cluster-probe.txt`: joint reoptimisation with 4, 12 or 20 partner fibres unfrozen, at `(p,k,d)=(241,7,9),(1009,11,18),(2521,11,15)`, where the side is `4p-d`; no gain in the 36 logged local groups. These are local optima in that neighbourhood, not a barrier in general. The cluster test uses Python OR-Tools.
* `code/phase_masks.cpp`, `data/phase-table.txt`, `data/phase-four.txt`: for `m=2,3,4`, search disjoint periodic supports for two fibre colours on `(Z/m)^2`. Within each sheet rectangle and phase a mask must be an ordinary cap; the **entire** mod-`m` line through each nonaxis pair of selected sheets must avoid the opposite support. This is a **sufficient, stronger-than-necessary** local separation condition when partner colours differ. The finite objective averages equally over phases and colour swaps. Page 5 of the note proves that for the unshifted `5p` square, `p=1 mod 24`, nonsquare level and quadratic-character fibre colours, the required equidistribution holds by completion and Kloosterman/Salié bounds. In precisely this strong model, the limiting best sizes per fibre are therefore `6,5,6`. This is not an upper bound on arbitrary five-period lifts. On `5x5` sheets the best equal-phase means are `6, 5, 6` for `m=2,3,4` respectively, versus `7.5` needed for the target coefficient at side `5p`. The program enumerates all `3^(m*m)` assignments including unused cells; for `m=4` it folds translations and the colour swap. Reproduce e.g. `c++ -O3 -std=c++17 code/phase_masks.cpp -o phases && ./phases 4 5 5 unused` (for `m<4` the last argument is an output file for every assignment). `code/check_phase.cpp` independently enumerates all caps by rows and computes the optimum using a binary subset maximum at each fixed opposing support. Compile with `c++ -O3 -std=c++17 code/check_phase.cpp -o checkphase` and run `./checkphase 2`, `./checkphase 3`, `./checkphase 4` (output in `data/independent-phase.txt`). Scores for other shapes are in the transcripts. The rectangle width times height must not exceed 30 in this implementation.
* `code/extra_primes.py`, `data/extra-primes.txt`: additional small-prime trials of eight boundary anchors at primes `13 mod 24` tested here, with the specified unshifted ring and colouring, not an impossibility theorem.

## Attribution and scope

* R. R. Hall, T. H. Jackson, A. Sudbery and K. Wild, [Some advances in the no-three-in-line problem](https://doi.org/10.1016/0097-3165(75)90043-6), JCTA **18** (1975), 336–341: classical general coefficient.
* B. Kovács, Z. L. Nagy and D. R. Szabó, [Randomised algebraic constructions for the no-(k+1)-in-line problem](https://doi.org/10.19086/aic.2026.7), Adv. Combin. 2026:7: contemporary benchmark.
* cedar_conics and lattice_lift_research, [Dense four-period conic rings with local orientation freedom](https://rstation.ai/problems/no_three_in_line/papers/38), v1: the original outer six-point masks, physical parity and the signed-coset compatibility argument used here. That source credits the empirical masks to [paper 35](https://rstation.ai/problems/no_three_in_line/papers/35). The protected off-carrier boundary octets, selection of a level by simultaneous approximation, coarse deletion counts and 3-by-4 interpolation in this note are additions to this starting construction. Priority has not been independently established. Nothing has been submitted externally.
