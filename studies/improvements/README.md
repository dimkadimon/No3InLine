# More points on the same board

**19 November 2026 · Ordinary Euclidean no-three-in-line problem.** All coordinates are integers, start at zero and lie in `[0,n-1] × [0,n-1]`. Read **`improved-bounds.pdf`** first: it gives the comparisons, diagrams from the actual coordinates, and the general construction with proof. Open **`explore.html`** to zoom into all seven constructions and switch among old points, exchanges and literal public extensions; all data are embedded locally. This is a research working note, not a peer-reviewed or submitted paper.

## Results

| Side | Identified public set¹ | Previous set in this project | This set | Net vs public | Net vs previous | Append without deleting any public point |
|---:|---:|---:|---:|---:|---:|:--|
| 16,018 | 24,306 | 24,469 | **24,588** | **+282** | +119 | **+2 exactly** |
| 32,002 | 48,421 | 48,661 | **48,838** | **+417** | +177 | **+3 exactly** |
| 64,006 | 96,816 | 97,008 | **97,062** | **+246** | +54 | **at least +4** |

¹ [rStation paper 47 v1, §8](https://rstation.ai/problems/no_three_in_line/papers/47). These are the sizes of actual published sets on these same boards, not upper bounds or a comprehensive world-record registry. The first two exact append statements apply only if **every** point in the corresponding published set stays put. In the third, our axis scan is complete on four specified lines only. Do not read these as maxima on the entire board when exchanges are permitted.

| Side | Preceding half-turn set | This set | Net gain | Symmetry of this set |
|---:|---:|---:|---:|---|
| 293 | 446 | **508** | +62 | quarter-turn (127 four-point orbits) |
| 389 | 594 | **668** | +74 | quarter-turn (167 four-point orbits) |
| 4,037 | 6,176 | **6,296** | +120 | half-turn (3,148 pairs) |
| 10,085 | 15,364 | **15,520** | +156 | half-turn (7,760 pairs) |

These four gains are **vs our own preceding constructions**, not vs a global catalogue. On side 293, cropping the 524-point side-300 source `runs/greedy/out_300_3.txt` in the [paper 22 v4 bank](https://rstation.ai/api/v1/papers/no_three_in_line_22/versions/4/supplement) to `[4,296]²` gives 504 (an ordinary cap); the gain vs that actual crop is **4**. At 389, we did not establish the previous public best. The qualitative difference at 4,037 and 10,085 is that the earlier optimizations kept a specified dense ring untouched, while the new sets are allowed to exchange old sites. Neither search proves the board optimum.

**Which part is uniform?** For every prime `p > 3` and `3p ≤ n ≤ 4p`, the updated half-turn guarantee is `2n − 2p − 12` instead of `2n − 2p − 16`. The parity- and residue-specific guarantees on page 3 are sharper. At `p = 2003, n = 8012` the two generators actually give 12,002 and 12,006. The machine-aided finite branch of the theorem reduces to 93 explicit small cap files. The infinite branch is proved with a lattice covering argument and small local masks; sampling the generator is not the proof. Use a prime just above `n/4` for sufficiently large arbitrary `n`, or the all-side script below for **every** positive `n`. There is no new leading coefficient above 3/2 or better exponent of the prime-gap term.

Even without this theorem the middle witness alone yields more than `3n/2` for **every side 31,669 through 32,558** by cropping or embedding. This is a finite interval. In general a `K`-point cap at side `a` guarantees `K − 4 max(a−n,0)` on side `n`, since every deleted row or column loses at most two points.

## Use a construction

No package installation, solver or Internet is needed. Python 3.9 or later. Do not use `python -O` (internal assertions are intentional).

```sh
python3 code/construct.py 32002 --ordinary --csv example.csv  # 48,838 points
python3 code/construct.py 293 --csv quarter-turn.csv          # 508 points
python3 code/construct.py 8000 --csv my-side.csv              # any positive side; centred half-turn
python3 code/chart_caps.py 2003 8012 --use-new --csv chart.csv # direct theorem construction
```

`coordinates/n<SIDE>.csv` contains **all points** for each of the seven highlighted sets. The compact formula for the large sets starts with the paper-47 frame, then applies `data/final-<p>.txt` in order (remove listed frame points, insert the remaining listed points). `data/orbits293.csv` and `data/orbits389.csv` give one representative per fourfold orbit. Rotate around the *actual* square centre: `(x,y) → (n−1−y,x)`. `data/append<SIDE>.json` gives the literal additions to the *public* comparison set; `data/literal-<p>.txt` describes that whole enlarged set as edits to the bare frame. The `individual_sites` field is exhaustive only where `whole_board` is true.

The general script compares explicit guarantees, not all embeddings, local-search runs, public seeds or possible crops. Its output is a lower bound, not an assertion that a larger finite cap is unknown. `--ordinary` includes the already-constructed half-turn option, allows changing the centre for embeddings/crops, and also tries the classical frame and the large edited sets.

## Recheck the evidence

Requires a C++17 compiler (`CXX=c++` by default). Everything is computed in a temporary directory. Search is **not** rerun to establish feasibility.

```sh
python3 verify.py             # complete witness checks, using the bundled free-site enumerations
python3 verify.py --rescan    # additionally regenerate those two enumerations and the four-axis scan
```

The verifier (1) checks file hashes, (2) reconstructs the large frame sets and public/previous comparisons, (3) tests exact primitive directions through every insertion and compares the C++-generated CSV with the released points, (4) checks the append-only claims against the complete lists or the stated partial pool, (5) runs an independent all-directions audit of the four rotational sets, (6) reproduces the entire finite branch of the general theorem, and (7) runs small-board full-geometry/larger-board on-conic regressions and arbitrary-side smoke tests. The two free-list rescans can be the slowest step. The included `data/reproduction.txt` records an actual run. No floating angular filter is used by the verifiers.

For a single large file:

```sh
c++ -O3 -std=c++17 code/verify_frame.cpp -o checkframe
./checkframe data/final-16001.txt expanded.csv
```

See **`SEARCH.md`** for the separate heuristic discovery recipe. `bounds.tex` and `figures/two-caps.pdf` are the typeset source; from this directory run `pdflatex bounds.tex` twice. `code/figure.py` optionally regenerates the figure with Matplotlib; this is the only non-standard Python dependency and is not used for construction or verification.

## Provenance and limitations

- For small controls the all-side generator can also use one full-size word per represented side in the [Flammenkamp catalogue](https://wwwhomes.uni-bielefeld.de/achim/no3in/download/all_known_solutions), as retrieved 19 November 2026. These 75 known examples are in `sources/catalogue-examples.csv`; none is a new discovery. `python3 code/catalogue_small.py` verifies them all offline with exact directions.
- `sources/insertions_*.txt` are the actual public additions in the [paper 47 v1 supplement](https://rstation.ai/api/v1/papers/no_three_in_line_47/versions/1/supplement). `public300-crop-seed.txt` is the specific paper 22 v4 member identified above. The small public-start control runs in `data/try*` gave no count improvement at sides 100, 200, 240, 300; they are not new records.
- `sources/edits_*.txt`, `free*.txt`, `scan*.dat`, `n201.csv` and `n202.csv` are earlier verified project certificates, seed-free lists, heuristic input pools or finite sets, as appropriate. `sources/seed*.csv` and `previous*.csv` are the earlier half-turn rings and augmented examples. `sources/prior-construction.pdf` supplies the preceding interpolation lemmas and baseline, including the earlier -16 estimate and its relation to prior work.
- Classical asymptotic density: [Hall, Jackson, Sudbery and Wild (1975)](https://doi.org/10.1016/0097-3165(75)90043-6). Four-sheet-per-direction mask and colouring antecedents: [rStation paper 38](https://rstation.ai/problems/no_three_in_line/papers/38). A new finite certificate or a reduction in additive losses is not an asymptotic density breakthrough. No assertion of worldwide priority is made.
- Proof development, implementation, discovery and writing were substantially AI-assisted. Independent checking code is not independent human peer review. No submission or external communication was made on the user's behalf.
