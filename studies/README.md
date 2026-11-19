# Historical studies

These folders retain the earlier project sources, checkers, search code, prior papers, data and original manifests. Their stand-alone READMEs describe historical bundles. Start with the [current preprint](../paper/main.pdf) and [current table](../results/lower-bounds.csv); where comparisons differ, use the current table and its source scope.

- `general-grids/`: anchored rings and baseline interpolation.
- `followup/`: seam improvements and exact opposite-pair packings **with particular rings frozen**.
- `improvements/`: revised all-side construction and the best exchanges/rotation witnesses, including the seven full coordinate files. Its 504-point crop at side 293 is not a world benchmark.
- `larger-grids/`: first larger-board exchange sets, two larger-side compact certificates and medium and symmetry experiments.
- `no3research/`: a separate symmetry-restricted census and ordinary full-size configurations. Upper bounds there must not be read as unrestricted upper bounds.

For the unmodified historical verifiers and their SHA256SUMS, restore the external source files with `python3 scripts/restore_inputs.py --fetch` from the release root. `python3 scripts/verify_release.py --expand-large` materializes the two deliberately omitted CSV files from the committed compact certificates and compares them to the original byte-level digests. Only redundant expanded data and separately sourced inputs are omitted; the 12-page paper and its own 15 certified lower bounds can be read and checked offline. A redundant stand-alone zip in the original general-grids directory was not copied; it is not part of that study's manifest.
