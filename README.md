# No3InLine

**A super-polylogarithmic excess in the no-three-in-line problem**  
Dmitry Kamenetsky · R3 illustrated working manuscript · author and independent review pending

**[Read the paper (PDF)](paper/main.pdf)** · [TeX and ancillary source](paper/arxiv-source.tar.gz) · [Standalone finite replay (ZIP)](paper/anc/no3-replay-r2.zip) · [Response to review](REVISION.md) · [Finite comparison table (CSV)](results/lower-bounds.csv) · [Verification transcripts](verification/) · [Source credits](THIRD_PARTY.md)

On a square of side `n`, let `F_ht(n)` be the maximum number of points with no three on an ordinary straight line, invariant under the half-turn about the board centre. The paper proves that for infinitely many primes `p ≡ 1 (mod 840)`, with `n = 4p + 1`,

> **F_ht(n) ≥ 3n/2 + 1/2 + exp(log p / (300 log log p)).**

The guaranteed surplus dominates every fixed power of `log n`, but is smaller than every positive power of `n`. This refines the **additive term on a subsequence**; it does not improve the classical all-sides leading coefficient, bound the actual excess from above, or establish a positive density of good sides. Hall–Jackson–Sudbery–Wild's native side is `2q` for prime `q`, not `4p+1`. No practical cutoff for the asymptotic estimate is claimed.

### Idea

Keep six sites on each of `p−1` hyperbola fibres and add eight boundary sites. Interior opposite pairs are proposed at a **single common level**. Separate the multiplicative cosets of the obstructing secant endpoints, discard conflicting proposals, and use one matching to orient the ring. Only the proposals are thinned: flipping an orientation never lowers the number of ring sites. The index of `⟨−1,3⟩` measures the room for this construction, and Stewart's cyclotomic prime-factor theorem supplies a sequence with large index. The finite certificates are illustrations and independent lower bounds, not assumptions in the proof.

![Two physical secants and the two distinct bits assigned to clear them](paper/figures/previews/matched-secants.png)

**Read the diagram:** keeping component 46,139 leaves one endpoint of the transposed secant absent; flipping 5,045 removes one endpoint of the original secant. Each fibre still contributes six sites. [See all three diagrams with explanations](paper/FIGURES.md).

**R3.** Lemma 3.1 displays the normalized character expansion and the correction at its shift roots. Sections 5–7 make the counting multiplicities, edge cases and powers of `L_p` explicit. Appendix A contains the finite examples; the four F† comparisons are reported-only. The project data did not change: the [commit-pinned finite kit](https://raw.githubusercontent.com/dimkadimon/No3InLine/e19b8a1b689eba392c7d26ec3733e88db566dc0e/paper/anc/no3-replay-r2.zip) has SHA-256 `238f38e60234b982cd0ba13045bfad4809fb00e764d0eb1278bfeb7378d6d9ca`. It is available separately, in the source tarball's `anc/` directory and in the reader PDF. This GitHub release is a working manuscript, not a journal publication or arXiv submission.

## Selected finite bounds

These are the project's explicit checked sets on the listed boards, not unrestricted optima. External counts below are measured on the same side after the stated transfer. Table 1 and the CSV give all **15 sides**, provenance, symmetry, and the separate excess over `3n/2`.

| Side | Project witness | External comparison | Difference |
|---:|---:|:---|---:|
| 293 | 508 (quarter-turn) | 512, reported on 288 and embedded | −4 |
| 389 | 668 (quarter-turn) | ≥652 from reported 696 on side 400 | +16 vs 652 |
| 773 | 1,188 (half-turn) | ≥1,244 from reported 1,352 on side 800 | −56 vs 1,244 |
| 4,037 | 6,296 (half-turn) | 6,118, reported side-4,006 augmented frame embedded | +178 |
| 10,085 | 15,520 (half-turn) | 15,120, four-period ring | +400 |
| 16,018 | 24,588 | 24,306, paper 47 §8, same board | +282 |
| 32,002 | 48,838 | 48,421, paper 47 §8, same board | +417 |
| 64,006 | 97,062 | 96,816, paper 47 §8, same board | +246 |

The **504** from an actual side-293 crop is reproducible but is not the strongest ordinary comparison: a 512-point set has been reported on a smaller board. Similarly, a direct prime embedding alone is an incomplete benchmark on several sides. A positive difference in the table is relative to its cited comparator, **not a world-record claim**. See `results/README.md` for the exact rule. Separately, the 4,782,972-point example on side 3,188,645 realizes the matching criterion with 144 clauses, 288 distinct endpoint cosets and 38 component flips; it is not a numerical test of the asymptotic cutoff.

## Reproduce the release

Use Python 3.9+ **without `-O`**, and a C++17 compiler (`c++` by default). The principal geometry and table checks use no network, solver or nonstandard Python packages. The **standalone ZIP**, which is also attached to the reader PDF, has its own README and manifest; these same offline checks run in an empty directory after unpacking it. On a typical workstation allow several minutes and several hundred MB of RAM, especially for the largest matching example.

```sh
python3 scripts/verify_release.py --hashes-only   # release integrity, seconds
python3 scripts/comparison.py                    # regenerate counts, check CSV and typeset rows
python3 scripts/verify_release.py                # all 15 manuscript witnesses, exact geometry
python3 scripts/audit_counting.py                # small exact diagnostics, not an asymptotic proof
python3 scripts/build_paper.py                   # needs TeX, qpdf, Poppler; full checkout, not the kit
```

The witness verifier reconstructs sets independently of the heuristic that found them. It compares released CSVs with compact certificates or exact digests, checks the actual geometric constraints, and reproduces the matching certificate byte-for-byte. `verification/witnesses-r3.txt` records an R3 replay from a clean extraction of the identical kit. These checks do **not** verify the asymptotic estimates by computer.

For the separately credited upstream comparisons and the older experimental packages:

```sh
python3 scripts/restore_inputs.py --fetch         # 159 pinned data files; see THIRD_PARTY.md
python3 scripts/comparison.py --audit-sources    # all 146 P22 input geometries and exact crop maxima
python3 scripts/check_public_frames.py           # recheck the three published P47 starting sets
python3 scripts/verify_release.py --expand-large # also create two optional 131074-/1000018-side CSVs
python3 studies/improvements/verify.py --rescan  # earlier all-board/axis rescans and finite-branch audits
python3 studies/larger-grids/verify.py           # earlier frame, deletion/cover, medium-board and gap checks
```

`restore_inputs.py` refuses unpinned source bytes. It can also work offline from the named, previously downloaded archives. Do not commit restored third-party files or the two regenerable large CSVs. Previous package READMEs describe the original standalone bundles; their manifests remain unchanged. On this checkout, restore their inputs first. The new proof, all of its finite certificates and the 15 project lower bounds are already checkable before that step.

## Where to look

| Path | Contents |
|:---|:---|
| `paper/` | Current named preprint, complete proof, four vector illustrations, bibliography, reader PDF and TeX-source archive with ancillary kit. |
| `results/` | Machine-readable comparison, exact crop results, source row indices, and reported benchmarks. |
| `unbounded-gain/` | Original working proof and the C++ matching builder, separate verifier and compact certificate. |
| `small-prime-examples/` | Six anchored rings and a credited catalogue control. Download/open `gallery.html` to inspect the actual points offline. |
| `studies/improvements/` | Best exchange/rotation sets, exact coordinate lists, frame edits, all-side generator and interactive `explore.html`. |
| `studies/followup/`, `studies/general-grids/` | Earlier anchored-ring and boundary/interpolation notes, generators, and frozen-ring certificates. |
| `studies/larger-grids/`, `studies/no3research/` | Earlier larger frames and separate full-square-symmetry census, with source, certificates, and independent checkers. |
| `scripts/`, `verification/` | Release-level replay/build scripts and actual run summaries. |

## Attribution and license

Dmitry Kamenetsky proposed this research. Responsibility for the manuscript rests with the named author. Proof development, implementation, search and writing were substantially AI-assisted. **His review is ongoing**; independently implemented checks are not independent human refereeing. The project has no assigned arXiv identifier in this release. Please cite the title and the Git revision or tagged version used. The earlier working notes are retained to document provenance, not as separate claims of refereed publication.

The [MIT License](LICENSE) covers original project work. Upstream coordinate sources, inferred benchmarks, prior theorems, catalogue words/control sets, and font subsets are separately credited in [THIRD_PARTY.md](THIRD_PARTY.md); no third-party license is being overwritten. For the maintainer's safe GitHub publication workflow see [PUBLISH.md](PUBLISH.md).
