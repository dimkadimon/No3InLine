// Exact counts on the odd or even n x n Euclidean grid with all square symmetries.
// g++ -std=c++17 -O3 dihedral.cpp -o dihedral; ./dihedral 41
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <set>
#include <string>
#include <vector>
using namespace std;
using word = uint64_t;
struct P {
  int x, y;
  bool operator<(const P &b) const { return x < b.x || (x == b.x && y < b.y); }
};
struct Orb {
  int a, b;
  word radii;
  vector<P> p;
}; // a,b = absolute doubled central coordinates
const int MAXW = 24;
using Mask = array<word, MAXW>;
int n, m, w, L;
bool dump = false, ceiling_only = false;
vector<Orb> O;
vector<int> label;
vector<Mask> bad, tri, inc;
Mask avail{};
vector<int> chosen, firstsol;
uint64_t nodes, answer;
int key(int a, int b) {
  if (a < b)
    swap(a, b);
  return a * (a - 1) / 2 + b;
}
void bit(Mask &s, int i) { s[i / 64] |= word(1) << (i % 64); }
template <class F> void ray(P a, P b, const F &fn) {
  int dx = b.x - a.x, dy = b.y - a.y, g = gcd(abs(dx), abs(dy));
  dx /= g;
  dy /= g;
  for (int sg : {-1, 1}) {
    int x = a.x + sg * dx, y = a.y + sg * dy;
    while (0 <= x && x < n && 0 <= y && y < n) {
      int q = label[y * n + x];
      if (q >= 0)
        fn(q);
      x += sg * dx;
      y += sg * dy;
    }
  }
}
void prepare() {
  m = n / 2;
  label.assign(n * n, -1);
  int first = (n % 2 ? 0 : 1);
  for (int a = first; a < n; a += 2)
    for (int b = max(first, a); b < n; b += 2) {
      if (!b)
        continue;
      set<P> pts;
      for (int sx : {-1, 1})
        for (int sy : {-1, 1}) {
          pts.insert({(n - 1 + sx * a) / 2, (n - 1 + sy * b) / 2});
          pts.insert({(n - 1 + sx * b) / 2, (n - 1 + sy * a) / 2});
        }
      word u = 0;
      for (int t : {a, b})
        if (t)
          u |= word(1) << ((t - 1) / 2);
      O.push_back({a, b, u, {pts.begin(), pts.end()}});
      for (P p : pts)
        label[p.y * n + p.x] = (int)O.size() - 1;
    }
  w = O.size();
  L = (w + 63) / 64;
  if (L > MAXW || m > 60)
    abort();
  bad.resize(w);
  tri.resize(w * (w - 1) / 2);
  inc.resize(m);
  for (int i = 0; i < w; i++) {
    bit(avail, i);
    for (int r = 0; r < m; r++)
      if (O[i].radii >> r & 1)
        bit(inc[r], i);
    // Any conflicting triple with two points of i can be moved by D4 so its first point is p[0].
    for (unsigned j = 1; j < O[i].p.size(); j++)
      ray(O[i].p[0], O[i].p[j], [&](int c) {
        if (c != i) {
          bit(bad[i], c);
          bit(bad[c], i);
        }
      });
    for (int j = 0; j < i; j++)
      if (!(O[i].radii & O[j].radii))
        for (P p : O[j].p)
          ray(O[i].p[0], p, [&](int c) {
            if (c != i && c != j)
              bit(tri[key(i, j)], c);
          });
  }
}
void dfs(const Mask &S, word left, int skip) {
  nodes++;
  if (__builtin_popcountll(left) == skip) {
    if (!answer)
      firstsol = chosen;
    if (dump) {
      cout << "solution";
      for (int i : chosen)
        cout << " " << O[i].a << "," << O[i].b;
      cout << "\n";
    }
    ++answer;
    return;
  }
  int best = 999, r = -1, zero = 0;
  word missing = 0;
  for (word f = left; f; f &= f - 1) {
    int a = __builtin_ctzll(f), c = 0;
    for (int z = 0; z < L; z++)
      c += __builtin_popcountll(S[z] & inc[a][z]);
    if (!c) {
      missing |= word(1) << a;
      if (++zero > skip)
        return;
    } else if (c < best) {
      best = c;
      r = a;
    }
  }
  left &= ~missing;
  skip -= zero;
  if (r < 0)
    return;
  // Partition on the unique orbit using radius r, or skip r. No overcounting of skipped radii.
  for (int z = 0; z < L; z++)
    for (word b = S[z] & inc[r][z]; b; b &= b - 1) {
      int u = 64 * z + __builtin_ctzll(b);
      word used = O[u].radii, rest = left & ~used;
      if (__builtin_popcountll(rest) < skip)
        continue;
      Mask F;
      for (int j = 0; j < L; j++)
        F[j] = S[j] & ~bad[u][j];
      for (word h = used; h; h &= h - 1) {
        auto &v = inc[__builtin_ctzll(h)];
        for (int j = 0; j < L; j++)
          F[j] &= ~v[j];
      }
      for (int a : chosen) {
        const Mask &v = tri[key(a, u)];
        for (int j = 0; j < L; j++)
          F[j] &= ~v[j];
      }
      chosen.push_back(u);
      dfs(F, rest, skip);
      chosen.pop_back();
    }
  if (skip) {
    Mask F;
    for (int j = 0; j < L; j++)
      F[j] = S[j] & ~inc[r][j];
    dfs(F, left & ~(word(1) << r), skip - 1);
  }
}
int main(int argc, char **argv) {
  if (argc < 2)
    return 2;
  int tier = -1;
  for (int i = 2; i < argc; ++i) {
    string s = argv[i];
    if (s == "--all")
      dump = true;
    else if (s == "--tier" && i + 1 < argc) {
      tier = atoi(argv[++i]);
      if (tier < 0)
        return 2;
    } else if (s == "--ceiling-only")
      ceiling_only = true;
    else
      return 2;
  }
  n = atoi(argv[1]);
  if (n < 2 || n > 100)
    return 2;
  prepare();
  if (tier >= m)
    return 2;
  for (int k = max(0, tier); k < m && (tier < 0 || k == tier); k++) {
    answer = nodes = 0;
    firstsol.clear();
    dfs(avail, (word(1) << m) - 1, k);
    cout << "n=" << n << " skipped=" << k << " size=" << 4 * (m - k) << " count=" << answer
         << " nodes=" << nodes << "\n"
         << flush;
    if (ceiling_only && !answer)
      return 0;
    if (answer) {
      cout << "witness";
      for (int i : firstsol)
        cout << " " << O[i].a << "," << O[i].b;
      cout << "\n";
      return 0;
    }
  }
  return tier >= 0 ? 0 : 1;
}
