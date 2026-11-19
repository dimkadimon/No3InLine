# Manuscript

**Dmitry Kamenetsky, *A super-polylogarithmic excess in the no-three-in-line problem*, 19 November 2026.** Author's draft for review; this is not a claim of acceptance, endorsement or arXiv submission.

- `main.pdf`: typeset paper with the complete proof, figure, comparison table and references.
- `arxiv-source.tar.gz`: only the six TeX files and one prebuilt vector figure needed by pdfLaTeX. Single root `main.tex` at the archive top level; no BibTeX, shell escape, external figures, special class, or network connection required. No arXiv identifier is assumed.
- `proof.tex`: geometric and arithmetic argument; `examples.tex`: numerical evidence and comparison methodology. Table row files are generated from `../scripts/comparison.py`. `../scripts/figure.py` recreates the figure from the side-293 certificate (optional Matplotlib dependency).

From the repository root, `python3 scripts/build_paper.py` creates the source tarball, unpacks its known members into an empty temporary directory and runs pdfLaTeX three times on that copy. Alternatively, unpack the tarball into an empty directory and run `pdflatex main.tex` twice. Needs ordinary LaTeX with AMS, Latin Modern, microtype, geometry, booktabs, graphicx, xcolor and hyperref. The bibliography is included as TeX. Different TeX Live and font versions can produce different PDF bytes. The appendix-free proof is not conditional on the numerical illustrations.

**Before submitting:** finish the author's proof and citation review, including the same-root lift estimate and the shared-level alteration; choose an appropriate submission category (math.CO is a natural candidate) and a license on the submission service. The repository's MIT notice is not an arXiv submission or a selection in arXiv's licensing UI.
