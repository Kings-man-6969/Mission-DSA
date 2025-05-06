int substrings(string n) {
    const int MOD = 1e9 + 7;
    long long result = 0;
    long long dp = n[0] - '0'; 
    result += dp;
    
    for (int i = 1; i < n.length(); i++) {
        dp = (dp * 10 + (i + 1) * (n[i] - '0')) % MOD;
        result = (result + dp) % MOD;
    }
    return (int)result;
}