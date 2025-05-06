string solve(int n) {
    long long i = 2;
    long long k = 9;
    while (k % n != 0 || k < n){
        bitset<16> b(i);
        k = stol(b.to_string())*9;
        i++;
    }
    return to_string(k);
}