#include <bits/stdc++.h>

using namespace std;

pair<string, string> split_into_ranges(const string& l) {
  auto f = l.find(',');
  string first_range = l.substr(0, f);
  string second_range = l.substr(f + 1);
  return {first_range, second_range};
}

pair<int, int> split_range(const string& range) {
  // find '-'
  auto f = range.find('-');
  int start = stoi(range.substr(0, f));
  int end = stoi(range.substr(f + 1));
  return {start, end};
}

int main() {
  int total{};

  string line;
  while (getline(cin, line)) {
    auto ranges = split_into_ranges(line);  // {"2-4", "4-6"}
    auto [a, b] = split_range(ranges.first);
    auto [c, d] = split_range(ranges.second);
    // logic
    if ((a >= c and a <= d) or (b >= c and b <= d) or (c >= a and c <= b) or
        (d >= a and d <= b)) {
      ++total;
    }
  }

  cout << "total: " << total << "\n";
  return 0;
}
