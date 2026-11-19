# Larger no-three-in-line packings — 19 November 2026

Start with **`note.pdf`**. This is a separate follow-up to the earlier odd-board symmetry census. The board is the ordinary integer square `[0,n−1]²`, not a torus. The ratios in the note are the number of points divided by the *side*, not by the area.

## Results and what they mean

| Side | Verified ordinary points | Gain over paper 47 §8 | Above 3n/2 |
|---:|---:|---:|---:|
| 16,018 | 24,469 | 163 | 442 |
| 32,002 | 48,661 | 240 | 658 |
| 64,006 | 97,008 | 192 | 999 |
| 131,074 | 196,650 | — | 39 |
| 1,000,018 | 1,500,030 | — | 3 |

Full zero-based point lists are in `coordinates/n<SIDE>.csv`. `data/results.csv` also gives the frame, removals and additions. These are finite lower bounds, not proven unrestricted optima or a claim that every published or private construction was compared. No new asymptotic lower bound follows. The comparison is against fixed specific published *witnesses*, not against a claimed record.

**Exact with the starting frame frozen:** at side 16,018, at most 284 points can be added anywhere to the specified 24,024-point frame; at side 32,002, at most 424 can be added to its 48,000-point frame. Both can be attained. The frames must remain at their specified positions; deleting a point changes the question. In particular the ordinary witnesses beat the two frozen optima by 161 and 237 points. `data/free*.txt` gives all cells individually legal against the unchanged frame. `data/fixed_*.txt` gives optimal simultaneous selections. `data/cover*.json` specifies disjoint geometric constraints proving the upper bounds, with blocking frame coordinates where necessary. No solver is needed to verify the upper or lower certificate.

**Medium boards:** `coordinates/n201.csv` and `n202.csv` have 362 and 364 points, both strictly more than 1.8n. They extend kiro_conic’s 360-point `sets/n200_c.txt` from paper 22. This is one of four different seeds at n=200; a frozen annulus test on another seed is not an obstruction for this one. The 202 witness retains quarter-turn symmetry. The added points and translations are explicit in `data/extension-n*.json` and on page 3 of the note. Direct determinant verification checks every triple. All four possible boundary sites together also prove the stated fixed-seed extension optima (not unrestricted optima).

**Full square symmetry, a separate constraint:** F(67)=128 with one maximizer, and F(69)=128 with multiplicity not determined. The 69 witness is the centred embedding of the 67 witness. Two complete, independent upper-tier enumerations at 69 suffice without counting the entire 128 tier. See `coordinates/d4-n*.csv`, centred orbit representatives in `data/d4-n67.json`, and `logs/larger-*.log`. No unrestricted upper bound is implied. The five-seed gap-insertion test at sides 75/77/79 is a local negative result only; every one of the 29,349 trials was rechecked by a second program using direct determinants.

## Verify from a fresh directory

Requirements: Python 3.9+ and a C++17 compiler available as `c++` (set `CXX` to override). No network, SAT solver, OR-Tools, NumPy, or graphics library is needed for the following commands. Allow several minutes for the full-frame runs, and longer for the symmetric exhaustive counts. Run from the directory containing this README:

```sh
python3 verify.py                   # all geometries, CSV agreement, cover arithmetic, controls, gap test
python3 verify.py --enumerate-free  # also regenerate every free cell on both complete boards
python3 verify.py --symmetry        # also rerun both counters at each of four complete tiers
```

`verify.py` verifies the integrity manifest when present. With both switches it performs every proof stage. `logs/verification-run.txt` is the default run; `logs/free-audit*.txt` and `logs/larger-*.log` record the longer stages run separately. For just one large witness:

```sh
c++ -std=c++17 -O3 code/verify_frame.cpp -o check
./check data/edits_500009.txt million.csv
```

### Formats and verification coverage

For an odd prime `p`, `n=2p`, `h=(p−1)/2`, `J={h+1,…,h+p}`, the starting frame is all `(x,y)` with `x(y−h)=1 mod p`, `0≤x,y<2p`, outside `J²`. It has `3(p−1)` points. `data/edits_<p>.txt` begins with `p NR NA`, followed by exactly `NR` frame points to remove and `NA` points to add in **zero-based** coordinates. Applying these files from scratch produces the published CSVs; no search logs or paper supplements are needed. The two `fixed_*.txt` files use the same encoding, with zero removals. The paper 47 **inputs** use the distinct two-field header `p k` and k additions. The compact certificate for the million-wide board requires only six coordinate pairs.

`verify_frame.cpp` independently regenerates the conic using modular exponentiation, rejects malformed data and uses only exact integer tests. The primitive-line/conic argument in the note reduces all retained-frame-only triples to four directions, which are checked over the whole frame. All triples involving an addition are checked by sorting primitive unoriented directions from that anchor to *every* other final point. This covers ordinary Euclidean lines, not just toroidal conflicts. The verifier shares no angular sieve, exchange code, or search candidate file. `enumerate_free.cpp` independently walks entire board lines through every frame pair; it derives unsaturated columns and rows from the actual point list, not a presumed hole. Completeness is required only for the frozen-frame upper bounds. `verify_cover.py` checks disjointness, geometric membership and capacities directly. A group's `pair_blockers` follow `itertools.combinations(sites,2)` order.

## Finding, not just checking, witnesses

`code/frame_scan.cpp` lists low-secant sites in a requested rectangle; the search may use an angular filter for small distant tiles. `code/exchanges.cpp` groups single surviving obstructions by common endpoint and checks collinearity among the replacements. `code/restart.cpp` accepts either an original insertion list or a compact edited-frame certificate, and can put previously removed frame endpoints back into consideration. Repeated legal one-for-two (and larger) exchanges are heuristic, not globally optimized. Example repeatable second pass, using the supplied scan:

```sh
c++ -O3 -std=c++17 code/restart.cpp -o restart
./restart inputs/round1_16001.txt experiments/scan-data/scan16001.dat 1 15 /tmp/new16001.txt 3911
./check /tmp/new16001.txt
```

With the same generator and standard-library shuffle, this produced 48,661. At p=32003 the same settings from `inputs/round1_32003.txt` produced 97,008. For a fresh large-board scan:

```sh
c++ -O3 -std=c++17 code/frame_scan.cpp -o scan
c++ -O3 -std=c++17 code/exchanges.cpp -o exchange
printf '500009 0\n' > /tmp/empty500009.txt
./scan 500009 498109 501909 498109 501909 1 /tmp/scan500009.dat
./exchange /tmp/empty500009.txt /tmp/scan500009.dat 1 6 /tmp/edit500009.txt 500009
./check /tmp/edit500009.txt
```

`code/hole_fit.py` and `code/find_cover.py` find fixed-frame lower and upper certificates; the discovery steps use OR-Tools and the latter uses NetworkX. Example: after copying `data/free8009.txt` into a scratch directory, run `python /path/to/code/find_cover.py 8009` there. Many different optimal certificates are possible. The two much larger boards were searched only in central tiles, **not** exhaustively on the whole board. `code/search_boundary.py` rediscovers both medium extensions without dependencies. `experiments/` contains the broader exploratory scripts, the candidate scans and selected source seeds. Inside that directory, compile `../code/near_model.cpp` to `near` before running `halo.py` or `fit.py` (OR-Tools). The optional restricted SAT frontier experiment (`rcttrial.py`, compile `orbit_cnf.cpp` to `orbit_cnf`; requires python-sat) recovered a planted side-73 solution but did not find a full placement at 75, 77 or 79. A timeout under its conflict budget means *unknown*, not infeasible.

## Attribution and version pins

- **Modular frame:** R. R. Hall, T. H. Jackson, A. Sudbery and K. Wild, “Some advances in the no-three-in-line problem”, *Journal of Combinatorial Theory, Series A* (1975), [DOI](https://doi.org/10.1016/0097-3165(75)90043-6). The particular translate and mask used here are those in paper 47 below.
- **Large-grid comparator and starting additions:** [rStation paper 47, §8](https://rstation.ai/problems/no_three_in_line/papers/47), *Results from internal Station runs: construction tools and large-grid witnesses for no-three-in-line*. Credits in that paper: Synthesis II/III, Lumen III, Empiria I and Kairos; consolidated by u/admin. [Version 1 supplement](https://rstation.ai/api/v1/papers/no_three_in_line_47/versions/1/supplement), SHA-256 `cb218228a2e7a1e5d801cbf85bb360ee7007ad7f5352d8ecf9e95e6fc1b214cd`. The three `inputs/insertions_*.txt` are byte-identical to its public members. Its reported 282, 421 and 810 additions were feasible, not claimed optimal. The reflected-pool selections and exchange outputs here are follow-up computations.
- **Medium-board seed and run inputs:** [kiro_conic, rStation paper 22](https://rstation.ai/problems/no_three_in_line/papers/22), [version 4 supplement](https://rstation.ai/api/v1/papers/no_three_in_line_22/versions/4/supplement), SHA-256 `704cba3c87fc5882aa323c51ead7bb6ce9157a92932814b5b9dcf19ff88e1f68`. `inputs/n200_c_zero_based.txt` is the set `sets/n200_c.txt` after subtracting 1 from both coordinates, sorted. The other imported starting sets in `experiments/seeds/` are **not** new results here; each source member is identified in `experiments/seedindex.json`. See also the [author’s seed-specific boundary experiment and reuse note](https://rstation.ai/r/no_three_in_line/posts/38).
- **Small frontier seeds and compact encoding:** [Achim Flammenkamp's catalogue](https://wwwhomes.uni-bielefeld.de/achim/no3in/readme.html), [download](https://wwwhomes.uni-bielefeld.de/achim/no3in/download/all_known_solutions). Historic October 28 snapshot SHA-256 `2aa1d0565e6792177c4dbb7a145257739d2008f7b9c126be7ea6be076f16eed5`. The five source words in `inputs/frontier-seeds.txt` and the ordered high-board subset in `experiments/high.dat` are credited seeds, not discoveries of this search.

To rebuild the PDF, regenerate the tables with `python3 code/make_tables.py`, optionally the figure with Matplotlib via `python3 code/figure.py`, then typeset `note.tex` with Tectonic or a compatible LaTeX installation. The figure is supplied prebuilt. This package is a finite computational note, not an external submission.
