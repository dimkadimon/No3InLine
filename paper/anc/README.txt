FINITE SUPPLEMENT: no3-replay-r2.zip

This is the same immutable R2 finite-data kit supplied with the R3 paper.
The geometry, counts, proof diagnostics and table data have not changed.
The 75-member ZIP includes a README and a SHA-256 manifest for the other
74 members. The full 40-character Git commit which first pinned this kit is
e19b8a1b689eba392c7d26ec3733e88db566dc0e.

ZIP SHA-256:
238f38e60234b982cd0ba13045bfad4809fb00e764d0eb1278bfeb7378d6d9ca

Unzip into an empty directory. From that directory run, without Python -O:
  python3 scripts/verify_release.py --hashes-only
  python3 scripts/comparison.py
  python3 scripts/verify_release.py
Python 3.9+ and a C++17 compiler suffice for these offline checks. The kit's
README explains full coordinate expansion and optional pinned external data.
The four F rows use reported external counts, not audited source coordinates.
These programs check finite illustrations, not the infinite-family theorem.

Public download, pinned to the original kit commit:
https://raw.githubusercontent.com/dimkadimon/No3InLine/e19b8a1b689eba392c7d26ec3733e88db566dc0e/paper/anc/no3-replay-r2.zip
The README inside that immutable kit describes the earlier R2 manuscript.
