# Fully symmetric no-three-in-line sets and an obstruction at order 47

Research draft and computational supplement · 19 November 2026.

**Read `manuscript.pdf` first.** `manuscript.tex` and `witness47.pdf` are the complete LaTeX source and vector figure. The paper concerns ordinary Euclidean collinearity, with all eight square symmetries imposed for the main census. The order-47 obstruction concerns all ordinary 94-point solutions, regardless of their symmetry. Two further results on the unrestricted problem are in `extras/field-notes.md`.

## Results and definitions

- `data/census.csv` gives the exact maximum and the number of maximizers for each odd board from 3 to 65. `data/tiers.csv` includes the empty higher tiers, not just the positive witnesses. Order 1 is excluded: it has only the centre and is not a multiple-of-four case.
- `F(47)=92`, attained just once. The four possible insertions have coordinates `(±7,±7)` about the centre; `(7,7)` is the midpoint of two selected points, `(5,9)` and `(9,5)`. Symmetry blocks the other three. This configuration is maximal even without symmetry. It is not largest without symmetry: ordinary 94-point configurations exist at order 47.
- The first odd board with symmetric defect 10 is 61: `F(61)=112`, with 295 maximizers. There are 24 configurations attaining the odd-board symmetry ceiling `2n−2` over the reported range. Of these, only the cross on the 3-board can be enlarged.
- **Every 94-point solution at order 47 contains at most 68 points forming a fully symmetric subset** (symmetries of the fixed board). At least 26 deletions are needed. The bound need not be sharp. Two distinct enumerations and row-obstruction tests agree on every tier and on the same 24 surviving subsets out of 10,916,935 tested. Exact unrestricted completion search rejects all 24.
- Separately: **13 ordinary 2n-point configurations absent up to all eight square isometries from the dated catalogue**, and a **ten-deletion local obstruction** for all five specified even-order seeds at the 75-, 77-, and 79-board frontiers. Neither means that a new unrestricted order was solved. The auxiliary local obstruction was checked by one exhaustive program and a small-board regression, not by the two dihedral census programs.

## Verify within seconds

Requires Python 3.9+; no third-party packages for verification. Run in this directory:

```sh
python3 verify.py
python3 reproduce.py --n 47 --both
python3 extras/core_completions.py
python3 extras/test_frontier.py
```

`verify.py` acts only on the supplied public data: it expands the coordinates, checks cardinality and every ordinary three-point determinant, checks all 24 ceiling witnesses for possible insertions, and reconstructs the supplementary 13 examples and verifies their exact stabilizers and mutual inequivalence. It also verifies all five frontier inputs. A coordinate file alone proves a lower bound, not optimality.

For the additional historical catalogue comparison, download the `all_known_solutions` file from [Flammenkamp's data directory](https://wwwhomes.uni-bielefeld.de/achim/no3in/download/) and run `python3 verify.py --catalogue /path/to/all_known_solutions`. The October 28 snapshot hash and comparison with later revisions are explained in `extras/field-notes.md`. No external data or Internet access is necessary to reproduce the dihedral census.

## Reproduce the exact counts

Use a modern GCC or Clang C++17 compiler (`CXX=c++` by default). Both programs are deterministic and single-threaded. For one board or the whole reported range:

```sh
python3 reproduce.py --n 61 --both
python3 reproduce.py --all --both
```

The largest tiers are substantial finite enumerations. They may take minutes or longer per tier on a single CPU; do not mistake a partially finished run for a zero. Fast tests: 33, 41 or 47. Each command compares its completed terminal counts with the CSV. The main counter processes all radii-omission tiers from zero until the first nonzero count. To enumerate the individual winning orbit lists as well:

```sh
c++ -std=c++17 -O3 -march=native dihedral.cpp -o dihedral
./dihedral 47 --all
./dihedral 47 --ceiling-only --all
c++ -std=c++17 -O3 -march=native line_audit.cpp -o line_audit
./line_audit 47 0
```

**Coordinate conventions matter.** The C++ main counter emits **doubled** absolute centred coordinates (to let the same engine also represent even boards). On the odd boards of the paper divide the two printed integers by two. The JSON files already contain the resulting ordinary centred magnitudes `(a,b)`. Take all sign choices and both coordinate orders, remove duplicates, and add `floor(n/2)` to each coordinate if zero-based board coordinates are desired. The expanded CSV is already zero-based.

The two counters share neither source nor precomputed conflicts: `dihedral.cpp` walks secants through orbit representatives and tracks bitsets of orbit IDs; `line_audit.cpp` walks maximal board lines and converts triples of actual cells into incompatibilities, tracking possible partners per magnitude. `--large-first` on the second executable reverses a tie-break (used in the recorded audit of orders 51–61 at k=0,1 and 63 at k=0); it changes the node counts but not the answer. The independent audit is reported tier by tier in `data/audit.csv`. The determinant verifier is a third geometry check. These are reproducible exhaustive calculations, not externally peer-reviewed findings or formally checked UNSAT proof traces.

## Reproduce the unrestricted order-47 obstruction

`python3 extras/reproduce_core.py --both` enumerates six exact-size tiers, tests whether each set could fit in any ordinary 94-point solution and reruns the final completion searches. Allow several minutes; it streams the large intermediate lists rather than storing them. `--max-omitted 2` is a quick test. Two routes are checked: `dihedral.cpp` piped into the individual-cell filter `extras/core_obstruction.cpp`, and `extras/core_lines.cpp`, using the independent line counter and orbit-level blocked additions. The final 24 residual cores are in `data/core47-residual.txt`; `python3 extras/core_completions.py` checks those with elementary determinant tests in a few seconds. The claims need both exhaustion of the symmetric tiers and testing of the survivors.

## Contents

| Path | Contents |
|---|---|
| `data/census.csv`, `data/tiers.csv` | Published quantities in this draft; exhaustive counts by tier |
| `data/witnesses.json`, `data/coordinates.csv` | One optimum per board, compressed and expanded |
| `data/ceiling_configurations.json` | All ceiling-attaining sets in the reported range |
| `data/primary-transcript.txt`, `data/audit.csv` | Primary output and comparison of completed independent runs |
| `data/catalogue_additions.json` | All supplementary ordinary solutions, credited seeds, exact edits |
| `data/catalogue-additions.txt`, `data/catalogue-coordinates.csv` | Catalogue words and coordinates for sharing |
| `data/core47-*`, `extras/core_*.{cpp,py}`, `extras/reproduce_core.py` | Unrestricted symmetry-core bound, tier counts, remaining cases and replay |
| `extras/field-notes.md`, `extras/repair*`, `extras/frontier-seeds.txt` | Local extension proof, five credited inputs and transcript |
| `comparison/` | Baseline table snapshot, related work and scope of priority search |
| `figure.py` | Optional figure regeneration with Matplotlib |

## Before an arXiv submission

The `full` column in [the published minimal-defect table](https://wwwhomes.uni-bielefeld.de/achim/no3in/table_min_defect), dated 3 May 2026, has no odd-order values after 39. We did not find a later matching census in the sources checked. A blank table cell does **not** establish first discovery. Ask the catalogue maintainer whether any counts or supplementary records are already known but not posted; rerun the check on an independent machine; add responsible human author(s), appropriate disclosure of AI assistance and a durable data link. This package was prepared with AI assistance and is a draft; nothing was submitted or sent externally.

To compile after editing: run `pdflatex manuscript.tex` twice, or `tectonic manuscript.tex`. Do not delete the figure PDF. The author field is intentionally empty. The ZIP of the complete study includes the PDF, source, data and replay programs.
