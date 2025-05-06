int nonDivisibleSubset(int k, vector<int> s) {
    vector<int> r(k);
    for (size_t i = 0; i < s.size(); i++) {
        r[s[i] % k]++;
    }
    r[k/2] = (k % 2 == 0) ? 1 : r[k/2];
    int c = (r[0] > 0) ? 1 : 0;
    for (size_t i = 1; i < k/2 + 1; i++) {
        c += (r[i] >= r[k-i]) ? r[i] : r[k-i];
    }
    return c;
}