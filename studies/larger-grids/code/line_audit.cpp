// Independent counter for odd boards only. No shared code or geometric conflict data.
// g++ -std=c++17 -O3 line_audit.cpp -o line_audit; ./line_audit 47 0
// Given n=2m+1, k: count sets using exactly m-k positive coordinate magnitudes.
#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>
using namespace std;
using U = uint64_t;
struct Row {
  int a, b;
};
int m, order, nr;
bool large_first = false;
vector<Row> rows;
vector<int> id;
vector<U> forbidden2, forbidden3; // exclusions stored as partner masks indexed by magnitude
vector<int> stackrows;
uint64_t leaves, visits;
int ix(int a, int b) { return a * (m + 1) + b; }
int pairno(int i, int j) { return i > j ? i * (i - 1) / 2 + j : j * (j - 1) / 2 + i; }
U bit(int a) { return U(1) << a; }
void forbid(U *v, int w) {
  auto [a, b] = rows[w];
  v[a] |= bit(b);
  if (a != b)
    v[b] |= bit(a);
}
void clauses() {
  id.resize((m + 1) * (m + 1));
  for (int b = 1; b <= m; ++b)
    for (int a = 0; a <= b; ++a) {
      id[ix(a, b)] = id[ix(b, a)] = static_cast<int>(rows.size());
      rows.push_back({a, b});
    }
  nr = rows.size();
  forbidden2.resize(nr * (m + 1));
  forbidden3.resize(size_t(nr) * (nr - 1) / 2 * (m + 1));
  // Every primitive board direction and every maximal line in that direction with three cells.
  // The centre, which is incompatible with every nontrivial orbit, is omitted.
  auto in = [](int x, int y) { return abs(x) <= m && abs(y) <= m; };
  vector<int> vec;
  for (int dx = 0; dx <= m; dx++)
    for (int dy = -m; dy <= m; dy++) {
      if ((dx == 0 && dy <= 0) || gcd(dx, abs(dy)) != 1)
        continue;
      for (int x = max(-m, -m - 2 * dx); x <= min(m, m - 2 * dx); ++x)
        for (int y = max(-m, -m - 2 * dy); y <= min(m, m - 2 * dy); ++y) {
          if (in(x - dx, y - dy))
            continue;
          vec.clear();
          for (int u = x, v = y; in(u, v); u += dx, v += dy)
            if (u || v)
              vec.push_back(id[ix(abs(u), abs(v))]);
          // Examine triples of actual board cells. Multiplicities of orbit labels matter.
          for (size_t i = 0; i < vec.size(); ++i)
            for (size_t j = 0; j < i; ++j)
              for (size_t k = 0; k < j; ++k) {
                int a = vec[i], b = vec[j], c = vec[k];
                if (a == b && b == c) {
                  cerr << "internal orbit error\n";
                  abort();
                }
                if (a == b || b == c || a == c) {
                  int h = a == b ? c : b;
                  if (a == h)
                    abort();
                  forbid(&forbidden2[a * (m + 1)], h);
                  forbid(&forbidden2[h * (m + 1)], a);
                } else {
                  forbid(&forbidden3[size_t(pairno(a, b)) * (m + 1)], c);
                  forbid(&forbidden3[size_t(pairno(a, c)) * (m + 1)], b);
                  forbid(&forbidden3[size_t(pairno(b, c)) * (m + 1)], a);
                }
              }
        }
    }
}
// Optional leaf consumer used only by the separate symmetry-core check.
#ifndef AUDIT_SOLUTION
#define AUDIT_SOLUTION() ((void)0)
#endif
void count(U unused, int skips, const U *opts) {
  ++visits;
  if (__builtin_popcountll(unused) < skips)
    return;
  if (__builtin_popcountll(unused) == skips) {
    ++leaves;
    AUDIT_SOLUTION();
    return;
  }
  int row = -1, nopts = m + 5;
  U domain = 0; // stable tie-break: first available magnitude
  for (U u = unused; u; u &= u - 1) {
    int i = __builtin_ctzll(u);
    U d = opts[i] & (unused | 1u);
    int size = __builtin_popcountll(d);
    if (!size && !skips)
      return;
    if (size < nopts || (large_first && size == nopts)) {
      row = i;
      domain = d;
      nopts = size;
    }
  }
  U other = unused ^ bit(row);
  if (skips)
    count(other, skips - 1, opts);
  for (U w = domain; w; w &= w - 1) {
    int b = __builtin_ctzll(w), r = id[ix(row, b)];
    U next = other & ~bit(b);
    if (__builtin_popcountll(next) < skips)
      continue;
    U v[64];
    const U *g = &forbidden2[r * (m + 1)];
    for (int i = 1; i <= m; i++)
      v[i] = opts[i] & ~g[i];
    for (int t : stackrows) {
      const U *h = &forbidden3[size_t(pairno(r, t)) * (m + 1)];
      for (int i = 1; i <= m; i++)
        v[i] &= ~h[i];
    }
    stackrows.push_back(r);
    count(next, skips, v);
    stackrows.pop_back();
  }
}
int main(int argc, char **argv) {
  if (argc != 3 && argc != 4)
    return 2;
  if (argc == 4) {
    if (string(argv[3]) != "--large-first")
      return 2;
    large_first = true;
  }
  order = atoi(argv[1]);
  int skips = atoi(argv[2]);
  if (order < 3 || order > 81 || !(order % 2) || skips < 0 || skips > order / 2)
    return 2;
  m = order / 2;
  clauses();
  U all = bit(m + 1) - 2;
  vector<U> a(m + 1, all | 1u);
  count(all, skips, a.data());
  cout << "n=" << order << " skipped=" << skips << " size=" << 4 * (m - skips)
       << " count=" << leaves << " nodes=" << visits << "\n";
  return 0;
}
