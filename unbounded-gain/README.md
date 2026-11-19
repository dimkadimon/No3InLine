# An unbounded additive gain for half-turn no-three-in-line sets

**19 November 2026 — working proof, not independently reviewed or submitted.** Read `unbounded-additive-gain.pdf` (eight pages); `proof.tex` is its complete source. No finite computation is an assumption in the infinite-family proof.

For infinitely many primes `p ≡ 1 (mod 840)`, a centred half-turn cap in the integer square of side `4p+1` has at least

> `6p + 2 + exp(log(p)/(300 log log(p)))` points.

The quantity compared against is the actual anchored-ring count `6p+2 = 3(4p+1)/2 + 1/2`, **not** a bound rounded to a smaller prime. All eight anchors and six points per nonzero conic fibre are retained in the final construction. The conic level and which six points are selected in each fibre may change. There is no claim about appending to an already frozen witness, a larger leading coefficient, efficacy at a specific small prime, or priority.

## For the proof reader

- §2: whole-component flips of the [four-period ring](https://rstation.ai/problems/no_three_in_line/papers/38), boundary rays, and matching. If all abscissa cosets of blocking endpoint occurrences are distinct, each bit occurs at most twice. Any `j` clauses then see at least `j` bits.
- §3: short physical slopes and short *ratios of the signed distances to the two endpoints* must both be protected. A fixed positive proportion of single-root/level samples pass the finite sign test. Other triple types are counted by the number of distinct proposed opposite pairs involved.
- §§4–5: at one root, the [rooted product identity](https://rstation.ai/problems/no_three_in_line/papers/45) supplies the hit probabilities. For distinct ordinary lines reducing to the same modular slope, equal endpoint residues produce two rank-one matrices differing by `pE`. The short filters rule out rank-one `E`; the rank-two cases cost `O(log(p)/p)`. For unequal modular slopes, equations (4) relate the four coordinate ratios. Large integer gcds are charged using the divisor second moment; bounded gcds are controlled by angular separation in a rectangle.
- §6: two independent candidate roots use the **same** level. An exceptional zero coefficient in the cross-root equation is counted separately rather than being divided out.
- §§7–8: propose `floor(min(I,√p)/(1+log(p))³)` pairs, with `I` the index of `⟨−1,3⟩` in the multiplicative group. For `I ≥ (1+log(p))²⁴`, the expected eligible stock is a positive fraction of the proposals and the expected number of conflicts between them is lower order. Remove at most one **proposal**, not an old ring point, per conflict. [Stewart, Theorem 1, eq. (7)](https://arxiv.org/pdf/1008.1274) supplies primes of sufficiently large index. No independence of surviving secants or tests conditioned on a common level is asserted.

## A finite example and its compact certificate

`p=797161`, `k=11`, side **3,188,645**, subgroup order 26. In the two representatives `(1591070,845785)` and `(845785,1591070)` and their half-turn mates, all four central points can be added under one choice of orientations. The two representatives give 144 potential nonaxial secants and 288 distinct endpoint cosets. A standard square/nonsquare orientation has 38 blocking secants in the two representatives; flipping 38 components disables all of them. Final count: **4,782,960 old + 8 anchors + 4 central = 4,782,972**. This illustrates the distinct-coset criterion, not the size of the asymptotic gain or a numerical record.

`data/certificate.txt` starts with `p level number_of_representatives number_of_flips`, then the representatives and the flipped component labels. A component label is the smallest positive residue in the union of a coset and its inverse partner. Baseline physical parity: even for square abscissas, odd otherwise. The eight anchors are the square-symmetry orbit of `(0,p)`. The certificate determines all points without a large CSV.

## Replay (offline)

Python 3.8+ and a C++17 compiler suffice. Use a temporary directory for binaries. The matching pass may use a few hundred MB of RAM; no solver is needed. Do not run Python with `-O` (checks use assertions).

```sh
python3 code/sample_root.py
python3 code/check_identities.py
w=$(mktemp -d)
c++ -O3 -std=c++17 code/match_example.cpp -o "$w/match"
c++ -O3 -std=c++17 code/verify_example.cpp -o "$w/verify"
"$w/match" > "$w/certificate.txt" 2> "$w/matching.txt"
diff data/certificate.txt "$w/certificate.txt"
diff data/matching.txt "$w/matching.txt"
"$w/verify" < data/certificate.txt
```

The checker reconstructs components by union-find, independently of the matching builder. It verifies the complete set of possible old triple directions using the conic and actual integer intercepts. For every anchor and inserted central site it checks the normalized direction to **every other final point**. The saved outputs are `data/{matching,verification,algebra-checks}.txt`. The small-field algebra tests and the explicit rank-two lift example are diagnostics, not proofs of the asymptotic counting estimates. To rebuild the PDF, run `pdflatex proof.tex` twice with the standard AMS, geometry, hyperref and Latin Modern packages.
