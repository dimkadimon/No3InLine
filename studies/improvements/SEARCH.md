# Optional: how the seven sets were found

Feasibility follows from the released coordinates and `verify.py`, not from reobtaining a stochastic search trajectory. These commands document the actual search parameters. Start in the supplement root. Use a fresh scratch directory (several hundred MB can be helpful); no scratch file is a required certificate.

```sh
export W=$(mktemp -d)
for a in pool line_walk orbit_walk central_scan enrich; do
  c++ -O3 -std=c++17 code/$a.cpp -o "$W/$a"
done
```

## Edited modular frames

The previous frame edits and partial low-secant scans are included in `sources/`. The first batch used all sites in each supplied scan with depth at most one plus the previous insertions, and all bare-frame points. The pool builder obtains exact line capacities by canonicalizing primitive slopes. This means the optimization on this *restricted pool* uses the real geometry; it does not make the pool exhaustive or the local-search result globally optimal.

```sh
for p in 8009 16001 32003; do
  python3 code/frame_input.py "$p" 1 | "$W/pool" "$W/m$p.bin"
  steps=1500000; seed=19273
  if [ "$p" = 32003 ]; then steps=2500000; seed=73107; fi
  "$W/line_walk" "$W/m$p.bin" "$steps" "$seed" "$W/w$p.ids"
  python3 code/materialize.py "$W/m$p.bin" "$W/w$p.ids" "$W/stage1-$p.txt"
done
```

This stage found 24,524 / 48,748 / 97,062. The first two scans also include depth-two sites. We added candidates on at least one blocking secant that meets a current deletion, and rebuilt the entire exact induced model. Points in `sources/scan32003.dat` have depths zero and one only; no claim that such depth-two sites are absent elsewhere.

```sh
for p in 8009 16001; do
  "$W/enrich" "$p" "$W/stage1-$p.txt" "sources/scan$p.dat" > "$W/en$p.txt"
  python3 code/frame_input.py "$p" 1 "$W/stage1-$p.txt" "$W/en$p.txt" | "$W/pool" "$W/en$p.bin"
  "$W/line_walk" "$W/en$p.bin" 3600000 17357 "$W/en$p.ids"
  python3 code/materialize.py "$W/en$p.bin" "$W/en$p.ids" "$W/final-$p.txt"
done
```

These runs reached 24,588 and 48,838. Exact replay of tie ordering can depend on platform and compiler; the archived `data/final-*.txt` are sufficient, portable certificates. The binary scratch models use native four-byte integers; do not interchange them across endiannesses. `enrich.cpp` is only a candidate finder. Nothing is deduced about sites it did not suggest.

## Quarter-turn sets without a prescribed core

`orbit_walk.cpp` operates on full orbits of grid points; it runs with order 4 here. The search space excludes the centre singleton on odd sides. It is not exhaustive. Warm-start the long pass from the shorter pass:

```sh
for n in 293 389; do
  "$W/orbit_walk" "$n" 4 35000 "$((93+n))" "$W/rot$n.csv"
  "$W/orbit_walk" "$n" 4 450000 "$((503+n))" "$W/bestrot$n.csv" "$W/rot$n.csv"
done
```

The 93 auxiliary small coordinates in `data/small/` were generated with order 4, 1,800 steps and seed `7583+n`, one run per side. Optimality is neither used nor claimed. The independent `code/check_charts.py` decides exactly which small boards need these coordinates and checks each required count.

## Large half-turn exchanges

Here the unit of optimization is a pair `(x,y),(n−1−x,n−1−y)`. The available pool includes all seed sites, the earlier frozen extensions and central sites meeting relatively few seed secants. Candidate-pair folds of noncentral lines retain capacity two. A line through the centre contains any admitted orbit twice, so its folded capacity is one. Complex-search line models are not used in final verification.

```sh
for n in 10085 4037; do
  d=1; if [ "$n" = 4037 ]; then d=2; fi
  "$W/central_scan" "$n" 2 "sources/seed$n.csv" > "$W/central$n.txt"
  python3 code/board_input.py "$n" "$d" < "$W/central$n.txt" | "$W/pool" "$W/board$n.bin"
  python3 code/fold.py "$W/board$n.bin" "$W/fold$n.bin"
  "$W/line_walk" "$W/fold$n.bin" 600000 39913 "$W/os$n.ids"
  python3 code/materialize.py "$W/fold$n.bin" "$W/os$n.ids" "$W/sym$n.csv"
done
```

The medium and large symmetric CSVs are checked by a completely different implementation: it runs from every actual point to every other actual point, with integer gcd and sorting. It does not assume any orbit construction, secant-count model or modular curve.
