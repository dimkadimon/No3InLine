// Read "solution ..." rows from dihedral --all and test a necessary condition for inclusion
// in an arbitrary (not necessarily symmetric) 2n-point no-three-in-line set.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
int main(int argc, char **argv) {
  if (argc != 2)
    return 2;
  int n = atoi(argv[1]);
  if (n < 3 || !(n % 2) || n > 99)
    return 2;
  const int N = n * n, m = n / 2;
  vector<uint16_t> d(size_t(N) * N); // unoriented reduced direction from each cell to each old site
  int top = 2 * n * n + 2 * n;
  vector<uint32_t> tag(top);
  uint32_t epoch = 0;
  for (int a = 0; a < N; ++a)
    for (int b = 0; b < a; ++b) {
      int dx = a % n - b % n, dy = a / n - b / n, g = gcd(abs(dx), abs(dy));
      dx /= g;
      dy /= g;
      if (dy < 0 || (!dy && dx < 0)) {
        dx = -dx;
        dy = -dy;
      }
      int k = dy * (2 * n - 1) + dx + n - 1;
      d[size_t(a) * N + b] = d[size_t(b) * N + a] = k;
    }
  long long tested = 0, refuted = 0;
  string s;
  int boardsize = 0;
  while (getline(cin, s)) {
    if (s.rfind("solution", 0) != 0)
      continue;
    istringstream line(s);
    string w;
    line >> w;
    set<int> cells;
    while (line >> w) {
      size_t j = w.find(',');
      if (j == string::npos)
        return 2;
      int u = stoi(w.substr(0, j)), v = stoi(w.substr(j + 1));
      if ((u | v) & 1 || u < 0 || v < u || v >= n)
        return 2;
      u /= 2;
      v /= 2;
      for (int a : {-1, 1})
        for (int b : {-1, 1}) {
          cells.insert((m + a * u) * n + m + b * v);
          cells.insert((m + a * v) * n + m + b * u);
        }
    }
    vector<int> P(cells.begin(), cells.end()), rows(n), cols(n), yoptions(n), xoptions(n);
    vector<char> occupied(N);
    if (tested && boardsize != int(P.size()))
      return 2;
    boardsize = int(P.size());
    for (int z : P) {
      occupied[z] = 1;
      ++rows[z / n];
      ++cols[z % n];
    }
    bool good = true;
    // Individual insertions into the fixed core; different possibilities may be mutually
    // incompatible.
    for (int y = 0; y < n && good; ++y)
      if (rows[y] < 2) {
        for (int x = 0; x < n; ++x)
          if (cols[x] < 2 && !occupied[y * n + x]) {
            int z = y * n + x;
            bool ok = true;
            if (++epoch == 0) {
              fill(tag.begin(), tag.end(), 0);
              ++epoch;
            }
            const auto *h = &d[size_t(z) * N];
            for (int t : P) {
              int k = h[t];
              if (tag[k] == epoch) {
                ok = false;
                break;
              }
              tag[k] = epoch;
            }
            if (ok) {
              ++yoptions[y];
              ++xoptions[x];
            }
          }
        if (rows[y] + yoptions[y] < 2)
          good = false;
      }
    for (int x = 0; x < n && good; ++x)
      if (cols[x] + xoptions[x] < 2)
        good = false;
    if (!good)
      ++refuted;
    else
      cout << s << "\n";
    ++tested;
  }
  cout << "n=" << n << " core_size=" << boardsize << " tested=" << tested
       << " row_or_column_obstructions=" << refuted << " survivors=" << tested - refuted << "\n";
  return 0;
}
