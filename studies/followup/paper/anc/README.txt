BOUNDARY AUGMENTATION AND SYMMETRIC INTERPOLATION FOR NO-THREE-IN-LINE SETS
Supplement to the unsigned working draft, 19 November 2026.

Coordinates are zero-based ordinary integer grid points, not toroidal lines.
The paper is ../main.tex; the only figure is ../ring.pdf. Compile with pdflatex twice
from the source root. Run these examples from this ancillary directory:

  python3 code/any_side.py 1009 --csv points.csv
  python3 code/any_side.py 1009 --ordinary --csv ordinary-points.csv
  python3 code/anchor_ring.py --p 73 --csv boundary-points.csv
  python3 code/seam_caps.py 5003 17712 --csv rectangular-points.csv
  python3 code/seam_caps.py 2003 8012 --unscaled
  python3 code/check_certificates.py
  python3 code/level_fractions.py
  python3 code/verify.py --rescan --seams

Python 3.10+ standard library and C++17 suffice, including for the independent
finite upper and lower checks. Do not run Python with -O: assertions are used.
The verification script uses CXX (default: c++) to compile in a temporary
directory. Allow a few minutes and around 130 MB or more RAM for the largest
exhaustive scan. The published rerun output is data/reproduction.txt.

The any-side generator returns a symmetric witness for every positive n, compares
conservative guarantees, and is not a full search. --ordinary permits asymmetric
embeddings or crops as well; never promises a board optimum. Points rather than
just counts can be written to CSV. The seam program implements the signed-cycle
and optional short-rectangle repairs of Theorem 1.2. With no option it tries to
find a suitable scale; --unscaled omits the search and still gives the uniform
bound. code/anchor_ring.py also contains the preceding, weaker rectangular rule.

THEOREM AND COMPUTATION CHECKS

* data/prime-certificates.csv: all 194 small exceptional moduli from Theorem 1.1,
  not a sample. code/check_certificates.py does not import the generator.
* code/test_seams.py: template checks and 712 parameter cases. code/check_stream.cpp
  independently checks bounds, uniqueness, half-turn symmetry and primitive
  unoriented integer directions to every other point. code/carrier_check.py
  adds eight larger cases checked on the conic with all relevant directions.
* data/seedN.csv: the specific 6p+2 anchored sets for the four rows. The seeds
  are regenerated from the given (p,k) and compared, independent of the search.
* data/freeN.csv: ALL individually unblocked sites for that specific frozen seed.
  With --rescan they are regenerated from the seed, without trusting the table,
  by tracing the whole physical line of each old pair. They need not be compatible together.
* data/augmentedN.csv: complete point sets of sizes 446, 594, 6176, 15364.
  code/frozen_proof.py derives the exact optimum for half-turn append-only
  extensions of each specified seed using a small hypergraph, not CP-SAT:

    N      old   free sites   orbits  graph edges  needed ternaries  best added
    293     440        8         4         2              0               6
    389     584       12         6         1              0              10
    4037   6056      184        92        82              4             120
    10085 15128      344       172       114              7             236

  The centre is not free in any row. Conflicts of two orbits are tested with
  one old point or by checking whether the orbits lie on a single central line.
  Each remaining 3-orbit collinearity supplies one ternary constraint. The
  recurrence forbids one vertex of an outstanding triple, then exactly solves
  a graph independent-set problem by splitting components, leaf reduction and
  inclusion/exclusion. A maximum in this model is NOT a board maximum.
* code/pack_free.py N is the optional discovery program, requiring OR-Tools
  (version used: 9.15.6755). It writes data/augmentedN.csv; run in a copy if
  preserving the archived witness. Neither reproduction nor verification needs it.

Proofs of the uniform and prime-dependent bounds are in the paper; tests are not
substitutes for those proofs. No independent human review or submission is implied.
