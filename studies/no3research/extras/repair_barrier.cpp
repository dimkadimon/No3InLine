// Exact bounded-deletion extension search. Lower-left embedding, unrestricted output.
#include <algorithm>
#include <array>
#include <cassert>
#include <fstream>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>
using namespace std;
const string AL =
    "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,.";
const int M = 90, V = M * M;
struct E {
  unsigned char a, b;
};
vector<E> bl[V];
int oc[V], p[2 * M], n, K, dx0[2 * M], dy0[2 * M];
bool gone[2 * M], added[V];
int r[M], c[M], A[130], D[130];
int depth = 0, del = 0;
string seed;
long long nodes = 0, hits = 0;
inline int X(int u) { return u % n; }
inline int Y(int u) { return u / n; }
inline bool col(int a, int b, int z) {
  return (X(a) - X(z)) * (Y(b) - Y(z)) == (X(b) - X(z)) * (Y(a) - Y(z));
}
void popd(int t) {
  while (del > t) {
    int i = D[--del];
    gone[i] = false;
    r[dy0[i]]++;
    c[dx0[i]]++;
  }
}
void rem(int i) {
  if (!gone[i]) {
    D[del++] = i;
    gone[i] = true;
    r[dy0[i]]--;
    c[dx0[i]]--;
  }
}
void rec();
void pairs(int z, int h) {
  for (int k = h; k < (int)bl[z].size(); k++) {
    auto [i, j] = bl[z][k];
    if (gone[i] || gone[j])
      continue;
    if (del == K)
      return;
    int old = del;
    rem(i);
    pairs(z, k + 1);
    popd(old);
    rem(j);
    pairs(z, k + 1);
    popd(old);
    return;
  }
  A[depth++] = z;
  added[z] = true;
  c[X(z)]++;
  r[Y(z)]++;
  rec();
  r[Y(z)]--;
  c[X(z)]--;
  added[z] = false;
  depth--;
}
inline int room(int z, int g) {
  for (E e : bl[z])
    if (!gone[e.a] && !gone[e.b] && --g < 0)
      break;
  return g;
}
void choose(int z) {
  if (room(z, K - del) < 0)
    return;
  int old = del;
  for (int j = 0; j < depth; j++) {
    for (int k = 0; k < j; k++)
      if (col(A[k], A[j], z)) {
        popd(old);
        return;
      }
    // Every old point on the line joining this and a pinned addition is forbidden.
    int u = X(z), v = Y(z), dx = X(A[j]) - u, dy = Y(A[j]) - v;
    int g = gcd(abs(dx), abs(dy));
    dx /= g;
    dy /= g;
    for (int sign : {1, -1})
      for (int x = u + sign * dx, y = v + sign * dy; x >= 0 && y >= 0 && x < n && y < n;
           x += sign * dx, y += sign * dy) {
        int i = oc[y * n + x];
        if (i >= 0 && !gone[i]) {
          if (del == K) {
            popd(old);
            return;
          }
          rem(i);
        }
      }
  }
  if (room(z, K - del) >= 0)
    pairs(z, 0);
  popd(old);
}
int orig, goal, ox = 0, oy = 0;
void rec() {
  nodes++;
  if (orig - del + depth >= goal) {
    cout << n << " " << seed << " " << ox << " " << oy << " " << del << " ";
    for (int a = 0; a < del; a++)
      cout << p[D[a]] << ",";
    cout << " +";
    for (int a = 0; a < depth; a++)
      cout << A[a] << ",";
    cout << "\n";
    hits++;
    return;
  }
  int delta = 2 * n - goal;
  assert(delta == 0 || delta == 1);
  // Choose a set of parallel deficient lines whose combined deficit exceeds delta.
  vector<int> bestv;
  int best = 2 * n + 1;
  bool have = false;
  for (int axis = 0; axis < 2; axis++) {
    vector<int> low;
    bool have1 = false;
    for (int l = 0; l < n; l++) {
      int used = axis ? c[l] : r[l];
      if (used >= 2)
        continue;
      vector<int> v;
      for (int i = 0; i < n; i++) {
        int z = axis ? i * n + l : l * n + i;
        if (oc[z] >= 0 || added[z])
          continue;
        if (del == K && (r[Y(z)] == 2 || c[X(z)] == 2))
          continue;
        if ((int)bl[z].size() > K || room(z, K - del) < 0)
          continue;
        v.push_back(z);
      }
      if (2 - used > delta) {
        if ((int)v.size() < 2 - used - delta)
          return;
        if ((int)v.size() < best) {
          best = v.size();
          bestv = v;
          have = true;
        }
      }
      if (delta == 1) {
        if (have1) {
          if ((int)(low.size() + v.size()) < best) {
            best = low.size() + v.size();
            bestv = low;
            bestv.insert(bestv.end(), v.begin(), v.end());
            have = true;
          }
        }
        if (!have1 || v.size() < low.size()) {
          low = v;
          have1 = true;
        }
      }
    }
  }
  assert(have);
  for (int z : bestv)
    choose(z);
}
void solve() {
  for (int z = 0; z < n * n; z++) {
    bl[z].clear();
    oc[z] = -1;
    added[z] = false;
  }
  fill(r, r + n, 0);
  fill(c, c + n, 0);
  orig = 0;
  int m = seed.size() / 2;
  for (int j = 0; j < 2 * m; j++) {
    int x = int(AL.find(seed[1 + j])) + ox, y = j / 2 + oy;
    if (x < 0 || y < 0 || x >= n || y >= n)
      continue;
    int i = orig++;
    p[i] = y * n + x;
    oc[p[i]] = i;
    dx0[i] = x;
    dy0[i] = y;
    gone[i] = false;
    r[y]++;
    c[x]++;
  }
  if (orig >= goal)
    return;
  for (int i = 0; i < orig; i++)
    for (int j = 0; j < i; j++) {
      int x = dx0[i], y = dy0[i], dx = dx0[j] - x, dy = dy0[j] - y, g = gcd(abs(dx), abs(dy));
      dx /= g;
      dy /= g;
      for (int s : {1, -1})
        for (int u = x + s * dx, v = y + s * dy; u >= 0 && u < n && v >= 0 && v < n;
             u += s * dx, v += s * dy) {
          int z = v * n + u;
          if (oc[z] == -1)
            bl[z].push_back(E{(unsigned char)i, (unsigned char)j});
        }
    }
  rec();
}
int main(int argc, char **argv) {
  if (argc != 2)
    return 2;
  K = stoi(argv[1]);
  if (K < 0 || K > 15)
    return 2;
  while (cin >> seed) {
    int m = seed.size() / 2;
    n = m + 1;
    goal = 2 * n - 1;
    if (n >= M || seed.size() != 2u * m + 1)
      return 2;
    for (int j = 1; j <= 2 * m; j++)
      if (AL.find(seed[j]) >= size_t(m))
        return 2;
    nodes = hits = 0;
    solve();
    cout << "seed=" << seed << " n=" << n << " removals_at_most=" << K << " goal=" << goal
         << " hits=" << hits << " nodes=" << nodes << "\n"
         << flush;
  }
}
