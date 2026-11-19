# Verification ledger · 19 November 2026

These are outputs of executed checks. They are not human attestations, solver proofs of unrestricted optimality, or a machine verification of the infinite-family theorem.

| Transcript | Check that produced it |
|:---|:---|
| `replay-r2.txt` | Full `verify_release.py --expand-large` from a clean extraction of the **portable kit**, including its 74-file manifest, the revised finite diagnostics and all project witnesses. |
| `external-r2.txt`, `p47-witnesses.txt` | Offline restoration of both pinned station supplements (154 outputs), audit of 146 K geometries/windows and full integer checks of the three **public S** frames and additions. F remains **reported only**. The longer log includes the source extensions at 201 and 202. |
| `counting-diagnostics.txt`, `exported-rings.txt` | Four signed cancellation rows, rectangle degeneracies and complete small-field exceptional systems; new coordinate exporter equals all six smaller CSVs byte-for-byte and emits the full 4,782,972-point CSV with recorded digest. |
| `manuscript-witnesses.txt` | `python3 scripts/verify_release.py --skip-manifest` during assembly, before writing the final manifest. Offline complete geometry coverage for the project column of all 15 paper rows. Negative/invalid configurations are not counted as improvements. |
| `matching.txt` | Small-field identities, sample-root replay, C++ clause builder matched to both golden outputs; separate ring checker on side 3,188,645. |
| `small-primes.txt` | `python3 small-prime-examples/verify.py`: seven reconstructed CSVs and exact-geometry checks, including the credited side-21 control. |
| `exchange-and-frame.txt` | `python3 studies/improvements/verify.py --rescan` with restored source inputs, including two complete free-site rescans and the limited four-axis scan. Also 93 finite-branch and 652 further whole-board test cases. |
| `large-and-medium.txt` | `python3 studies/larger-grids/verify.py` including independent frame expansion, comparison with the two large historical CSVs, medium determinants, frozen covers and gap checks. |
| `source-pins.txt`, `comparisons.txt` | Pinned upstream inputs reproduced and all 159 output hashes checked; 146 P22 seed geometries and exact crop maxima audited; publication rows reproduced. The F-source results remain **reported** counts; they were not independently verified as coordinates. |
| `paper-build.txt` | R2: clean three-pass source-archive build, PDF attachment extraction and byte comparison, unchanged page text, and repeat-build agreement. Ten source archive members including the separate ancillary ZIP. |

For later replays run `python3 scripts/verify_release.py` **without** `--skip-manifest`. Other, earlier study-specific transcripts are preserved under their historical directories. Do not read the various experiments as independent replications by different groups: the checkers were separately written and run as part of the same AI-assisted project.
