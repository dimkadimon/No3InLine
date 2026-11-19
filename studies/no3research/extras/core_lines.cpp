// Independent census and extension obstruction for the focused order-47 calculation.
// Reuses the second, maximal-line counter, not the main orbit-ray counter or its extension filter.
// Pass the omission tier 0,...,5 as the only argument. Positive representatives output doubled.
#include <array>
#include <limits>
#include <map>
void test_core_leaf();
#define AUDIT_SOLUTION() test_core_leaf()
#define main line_audit_unused_main
#include "../line_audit.cpp"
#undef main
using BM = std::array<uint64_t, 5>;
std::vector<BM> excludes;
uint64_t pass = 0;
void prepare_core() {
  if (nr > 320)
    std::abort();
  excludes.resize(size_t(nr) * nr);
  // At q=(a,b) enumerate all other noncentral board cells grouped by their actual line with q.
  // Any two cells in such a group block q if their orbit(s) have been selected.
  for (int q = 0; q < nr; ++q) {
    auto [qx, qy] = rows[q];
    std::map<std::pair<int, int>, std::vector<int>> groups;
    for (int y = -m; y <= m; ++y)
      for (int x = -m; x <= m; ++x) {
        int dx = x - qx, dy = y - qy;
        if ((!x && !y) || (!dx && !dy))
          continue;
        int g = std::gcd(std::abs(dx), std::abs(dy));
        dx /= g;
        dy /= g;
        if (dx < 0 || (!dx && dy < 0)) {
          dx = -dx;
          dy = -dy;
        }
        groups[{dx, dy}].push_back(id[ix(std::abs(x), std::abs(y))]);
      }
    for (const auto &kv : groups) {
      const auto &v = kv.second;
      for (size_t i = 1; i < v.size(); i++)
        for (size_t j = 0; j < i; j++) {
          auto h = v[i], t = v[j];
          excludes[h * nr + t][q / 64] |= bit(q % 64);
          excludes[t * nr + h][q / 64] |= bit(q % 64);
        }
    }
  }
}
void test_core_leaf() {
  BM no{};
  unsigned margin[24]{};
  for (size_t i = 0; i < stackrows.size(); ++i) {
    auto u = stackrows[i];
    no[u / 64] |= bit(u % 64); // already occupied
    auto [a, b] = rows[u];
    margin[a] = 2;
    margin[b] = (a == 0 ? 1 : 2);
    for (size_t j = 0; j <= i; ++j) {
      auto &v = excludes[u * nr + stackrows[j]];
      for (int t = 0; t < 5; ++t)
        no[t] |= v[t];
    }
  }
  // Centre is blocked by an opposite pair. By transposition each column has the same options as its
  // row.
  for (int y = 0; y <= m; ++y)
    if (margin[y] < 2) {
      unsigned options = margin[y];
      for (int x = 0; x <= m && options < 2; ++x)
        if ((x || y) && margin[x] < 2) {
          int q = id[ix(y, x)];
          if (!(no[q / 64] & bit(q % 64)))
            options += 1 + (x != 0);
        }
      if (options < 2)
        return;
    }
  ++pass;
  std::cout << "solution";
  for (int u : stackrows)
    std::cout << " " << 2 * rows[u].a << "," << 2 * rows[u].b;
  std::cout << "\n";
}
int main(int argc, char **argv) {
  if (argc != 2)
    return 2;
  int k = std::atoi(argv[1]);
  if (k < 0 || k > 5)
    return 2;
  order = 47;
  m = 23;
  clauses();
  prepare_core();
  U all = bit(m + 1) - 2;
  std::vector<U> a(m + 1, all | 1u);
  count(all, k, a.data());
  std::cout << "n=47 core_size=" << 4 * (m - k) << " tested=" << leaves
            << " row_or_column_obstructions=" << (leaves - pass) << " survivors=" << pass << "\n";
  return 0;
}
