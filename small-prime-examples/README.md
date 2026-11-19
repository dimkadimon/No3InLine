# Small-prime examples for the half-turn additive-gain question

Open **gallery.html** to see the actual points and compare the two orientations at `p=73`. Both the displayed diagrams and `coordinates/p*.csv` use zero-based coordinates. No online resources or packages are needed to use the gallery. This supplement contains finite certificates, **not** a numerical test of an asymptotic growth law.

| p | side n | conic level k | flipped component labels | ring + 8 anchors | additional central points | total | total − 3n/2 |
|---:|---:|---:|:---|---:|---:|---:|---:|
| 73 | 293 | 28 | 1 | 440 | 10 | 450 | 10.5 |
| 97 | 389 | 17 | none | 584 | 10 | 594 | 10.5 |
| 193 | 773 | 20 | 2 | 1,160 | 28 | 1,188 | 28.5 |
| 2,521 | 10,085 | 11 | none | 15,128 | 236 | 15,364 | 236.5 |
| 3,361 | 13,445 | 11 | none | 20,168 | 292 | 20,460 | 292.5 |
| 4,201 | 16,805 | 11 | none | 25,208 | 300 | 25,508 | 300.5 |

The first three primes are smaller analogues congruent to 1 modulo 24. The last three are the *first three primes* congruent to 1 modulo 840. Being in this congruence class is necessary for the prime sequence in the working theorem, not sufficient for its large-index hypothesis. All six rows are actual witnesses checked directly, not promises for every prime. These are not claims of unrestricted optimality or records. For a tiny, separate example we include a 42-point half-turn optimum at `p=5`, side 21, decoded from [Achim Flammenkamp's catalogue](https://wwwhomes.uni-bielefeld.de/achim/no3in/download/); this example is **not** an anchored ring.

## Exact certificate convention

Set `t=4p`. There are 6 points above each residue pair `(u,k/u)`, `1≤u<p`. Take the physical points `(u+i p, v+j p)`, `v=k/u mod p` in `1..p-1`, for `0≤i,j≤3` on the boundary of the four-by-four sheet square (at least one index is 0 or 3) and having `x+y` even for square `u`, odd otherwise. Flip this parity on the specified components; a label is the smallest positive member of the set closed under `u↦−u`, `u↦3u`, `u↦k/u` modulo `p`. These flips preserve the 6-per-fibre count. The eight anchors are the orbit of `(0,p)` under the symmetries of the square. For each supplied representative `(x,y)`, include both it and `(t−x,t−y)`.

`examples.json` contains all the input parameters. A text certificate starts with `p level number_of_representatives number_of_flips`, followed by those representatives and flip labels. At `p=73`, level `28`, the flipped component is `H ∪ 28H` for `H=⟨−1,3⟩`. Its five representatives are `(115,130), (117,142), (121,185), (131,122), (138,131)`. The pre-flip ring contains `(96,52)` and `(193,246)` on `y=2x−140`, which blocks `(131,122)`. The latter old point is removed in the flip and the former stays. The whole final set, not only this line, was verified.

At `p=73,193` examples were obtained by testing anchored-ring orientations, enumerating individually available points and collecting mutually compatible opposite pairs. `p=97,2521` reproduce existing frozen-ring certificates in this project. For `p=3361,4201` all seed-pair lines were rasterized in the central square; a finite integer program packed opposite pairs subject to mixed-pair conflicts and all-new triples. Reported counts require only feasibility, not solver optimality.

## Verify

Python 3.8+ and a C++17 compiler (`CXX`, default `c++`) are needed. Run `python3 verify.py` without `-O`. It independently reconstructs the full CSV sets from the compact parameters, checks cardinality, bounds and half-turn closure, and:

- for `p≤193`, checks all primitive unoriented directions from every point for duplicates;
- for the three larger primes, uses `check_ring.cpp` to derive the possible same-fibre directions, scan actual old integer line intercepts in each, and check every ordinary direction from each anchor/central point to all the other final points. Completeness for old triples follows because an ordinary primitive line meets the modular conic in at most two distinct residues.

`verification.txt` is the recorded successful replay. No MIP or other solver is used by the verifier.

## What the comparison means

Hall–Jackson–Sudbery–Wild, [Theorem 2 and its corollary (1975)](https://www.sciencedirect.com/science/article/pii/0097316575900436), gave `3(q−1)` points on side `2q` and the asymptotic `1.5n−o(n)` lower guarantee for arbitrary large sides. The positive finite excesses over **3n/2 itself** in the table are distinct from the gain over embedding their construction at a smaller prime. The working infinite-family claim is a super-polylogarithmic but subpolynomial guaranteed surplus on selected sides; it does not increase the leading coefficient. The construction and proof have not been independently reviewed for correctness or priority.
