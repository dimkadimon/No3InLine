# How the construction works

The square is an ordinary integer board. A picture of lines modulo a prime alone would not certify a no-three-in-line configuration: the construction must also rule out triples on physical lines.

## 1. Swap six sites for six

![The physical board, eight boundary anchors, and the two complementary masks of a single residue fibre](figures/previews/ring-and-masks.png)

The eight squares sit on the boundary. The ring leaves the middle block free; proposed insertions come in half-turn pairs there. On the left, only the lifts of one residue pair, `(47,27)` at `p=73, k=28`, are shown. On the right, the outlined cell changes from filled to empty. It contains `(193,246)`, one of two ring points that initially block the proposal `(131,122)` on the line `y = 2x − 140`. Flipping the entire component clears this endpoint without reducing the number of ring points. The other ring fibres are omitted, **not** empty. [Vector diagram](figures/ring-and-masks.pdf) · [Complete 450-point finite example](figures/one-flip.pdf)

## 2. Match blocking pairs to orientation bits

![A pair of transposed secants; the two clauses use four endpoint cosets but can be assigned two distinct bits](figures/previews/matched-secants.png)

This is a fragment of the actual side-3,188,645 witness, not a generic cartoon. At `q=(1591070,845785)`, the two old endpoints are `P=q+155653(3,11)` and `S=q−14051(3,11)`. The other representative is the transpose of `q`, so its endpoints are the transposes of `P` and `S`. A clause asks that at least one of its endpoints be absent. The matching assigns one bit to each clause:

| Assigned bit | Choice | Endpoint absent as a result |
|---:|---|---|
| 5,045 | Flip the whole component | `S` at `q` |
| 46,139 | Keep the original orientation | `Pᵀ` at `qᵀ` |

The four endpoint occurrences have different abscissa cosets. Transposition exchanges the two cosets of a bit, so only two bits appear. The half-turn mates of the two targets are **different from the transpose** and are protected by reflection. In the full certificate, 144 clauses are matched and 38 bits are flipped. [Vector diagram](figures/matched-secants.pdf) · [Exact coordinates and bit labels](../results/diagram-endpoints.csv)

## 3. Thin the proposals, not the ring

![Illustrative conflict hypergraph before and after deleting one proposal per marked conflict](figures/previews/shared-level-selection.png)

Every numbered vertex represents **two** proposed sites at the same level. Here one pair and one triple of indices are marked as incompatible. Discarding indices 2 and 4 removes both obstructions; the four survivors supply eight sites once their clauses are matched. This is a schematic of the deletion argument in Proposition 7.2, not a numerical sample or an estimate of the asymptotic gain. [Vector diagram](figures/shared-level-selection.pdf)

To regenerate these three figures and the four-row endpoint CSV from the released certificates, run `python3 scripts/construction_diagrams.py --previews paper/figures/previews` from the repository root (requires Matplotlib). The TeX archive already contains the vector PDFs and needs no graphics-generation software.
