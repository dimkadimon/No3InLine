# The ordinary square-grid problem: separate results

These are **not** upper bounds on the unrestricted maximum and are distinct from the fully symmetric census in the manuscript.

## 13 additional configurations of size 2n

The files `../data/catalogue_additions.json`, `../data/catalogue-additions.txt` and `../data/catalogue-coordinates.csv` contain the same 13 configurations in reconstructible, compact and coordinate form. We used an ordinary (not toroidal) board for validation. Twelve configurations have trivial square stabilizer; the order-36 example has exactly half-turn symmetry. The orders, with repetitions, are 21 (3), 23, 25, 27, 29, 30 (3), 31, 36 and 56. These are genuinely maximum **in size** by the two-per-row bound, but none is the first 2n-point witness for its board size.

The October 28, 2026 snapshot of Achim Flammenkamp's `all_known_solutions` file contains 431,017 rows. None of the eight images of any of the 13 sets occurs there. For example, it contains five explicitly coded asymmetric solutions at order 56; the new 112-point example gives a sixth inequivalent configuration. The claim is absence from that dated snapshot, not absence from every private or public collection in existence. Credit for the starting configurations belongs to the original constructors and catalogue; each exact source word is in the JSON. The digit alphabet and row-major, two-columns-per-row format are Flammenkamp's. The new words are normalized by least row word among the eight square isometries; this convention need not be his display orientation.

**How to reproduce them.** For seven seeds the operation is just a cyclic change of the row or column origin: send (x,y) to ((x−xcut) mod n, (y−ycut) mod n). Although this preserves the two-per-row/column rule, it does NOT preserve Euclidean noncollinearity in general. For four other seeds the operation is a balanced exchange. In the remaining two cases, translate a neighbouring-order seed by the listed offset, intersect it with the destination board, then apply the specified exchange. Each edit list is in the destination's zero-based coordinates. `verify.py` reconstructs all 13 from their sources, tests every integer determinant, checks their stabilizers and tests inequivalence. With `--catalogue` it also checks that all seed words were present and that no final image is in the supplied snapshot. No network connection is required for the geometry tests.

Archive URL: https://wwwhomes.uni-bielefeld.de/achim/no3in/download/all_known_solutions  
Historical SHA-256: `2aa1d0565e6792177c4dbb7a145257739d2008f7b9c126be7ea6be076f16eed5`.

## Why a small repair does not fill the 75- and 77-board gaps

Embed a catalogue m-board in a corner of the (m+1)-board, with no distortion. Write S for its 2m occupied sites. For each of the two published m=74 sets, each of the two m=76 sets, and the single m=78 set in the snapshot, we searched the following question **without any symmetry constraint on the result**:

> Is there a valid T on the larger board with |T| ≥ 2m+1 and |S minus T| ≤ 10?

The answer was no for all five specified seeds. Thus gaining even one point from any of these embeddings requires discarding **at least eleven original points**. This is only a local obstruction. It is not a proof that 149, 153, or 157 points are impossible on the respective boards. The four possible corner embeddings give isomorphic searches because each seed is quarter-turn invariant.

| Larger board | Target | Recursive calls, seed order as in `frontier-seeds.txt` | Hits |
|---:|---:|---|---:|
| 75 | 149 | 525854; 450042 | 0 |
| 77 | 153 | 749925; 286645 | 0 |
| 79 | 157 | 466996 | 0 |

**Reproduction.** `c++ -O3 -std=c++17 repair_barrier.cpp -o barrier && ./barrier 10 < frontier-seeds.txt`. The five input rows are credited to Flammenkamp's archive, not new configurations. The recorded output is in `repair-transcript.txt`. This auxiliary negative result uses one exhaustive implementation, not the two counters used for the main symmetry census.

**Why this local test is exhaustive.** Keep a valid partial set consisting of retained old points and committed new points. Never reinsert a deleted old point on that branch. To reach 2n−1, at most one unit of row deficiency, and at most one unit of column deficiency, may remain. A row currently deficient by two must receive an addition; at least one of any pair of deficient rows must receive an addition. The same holds for columns. Pick one such line or pair of lines and branch over admissible new cells in it. For a trial cell q, every retained old pair on a secant through q must lose an endpoint. Pairs on different such lines are disjoint, giving a lower bound on the deletion budget required. Branch on the endpoint to delete. A line through q and one earlier committed addition forces the deletion of every retained old site on it. Two earlier committed points collinear with q rule it out. These are all possible new triples. If a target T exists, at least one branch chooses a point of T and deletes only points outside T at each step. A target is therefore not lost by the pruning. Branch duplication is harmless for a zero-hit test.
