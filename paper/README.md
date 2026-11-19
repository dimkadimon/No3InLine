# Manuscript · R2

**Dmitry Kamenetsky, *A super-polylogarithmic excess in the no-three-in-line problem*, revised working manuscript, 19 November 2026.** Author review in progress. No claim of acceptance, endorsement, public archival release or arXiv submission. [Changes in response to review](../REVISION.md).

- `main.pdf`: reader edition. It includes an attachment `no3-replay-r2.zip` with the finite-data kit. Download the PDF if a browser does not show its attachments pane. Alternatively run `pdfdetach -save 1 -o replay.zip main.pdf` or take `anc/no3-replay-r2.zip` directly.
- `arxiv-source.tar.gz`: one top-level `main.tex`, its seven other TeX inputs, one prebuilt vector figure and the replay ZIP under `anc/`. The TeX source **never reads `anc/`**. A normal pdfLaTeX processor produces the same pages without the optional attachment; the ancillary file remains accessible in the supplied archive. See [arXiv's ancillary-files guidance](https://info.arxiv.org/help/ancillary_files.html).
- `proof.tex`: ring, sign sieve, geometric exclusions, sampling, exhaustive triple table and prime sequence. `collisions.tex`: standalone proofs for equal modular slopes, the four large-gcd cases, directions in rectangles, both dyadic regimes, and shared-level root pairs.
- `examples.tex`: Appendix A, finite evidence. `reproduction.tex`: Appendix B, data availability and replay. `references.tex`: bibliography. The two table fragments are checked by `../scripts/comparison.py`; `../scripts/figure.py` regenerates the figure (optional Matplotlib).

To typeset from the supplied source, unpack into an empty directory and run `pdflatex -no-shell-escape main.tex` three times. Requires standard AMS, Latin Modern, microtype, geometry, booktabs, tabularx, graphicx, xcolor and hyperref. There is no custom class, BibTeX, required shell escape, external figure or network access. No finite checker needs to run to compile or read the proof.

From the full repository, `python3 scripts/build_paper.py` makes the tarball and compiles from a fresh unpack. It also uses `qpdf` (tested with 12.2.0) to attach the immutable replay kit to the distribution PDF, and `pdfdetach` and `pdftotext` from Poppler to check the exact attachment and unchanged page text. On the recorded toolchain repeated builds produced identical PDF and tarball bytes. TeX/font, compression and PDF tool versions can affect cross-machine binary reproducibility.

**Versions.** The portable kit and finite code have local Git revision `e19b8a1b689eba392c7d26ec3733e88db566dc0e`; the revised manuscript is identified in the full Git bundle by the local tag `review-r2-2026-11-19`. The unchanged historical data and most of the core checkers were already present at `27975940dc0d3201c3b2dda0a230c52740ec25f6` (the reviewed 12-page draft). The kit, not the full Git bundle, is embedded in `main.pdf`.

Before submission, complete the author's proof, source, attribution and rights review, seek expert scrutiny, and supply the verified public archival link if one is established. The repository's MIT notice is not an arXiv submission or a selection in arXiv's licensing UI.
