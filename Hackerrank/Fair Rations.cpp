string fairRations(vector<int> B) {
    int res = 0;
    for(int i = 0; i < B.size() - 1; i++){
        if(B[i] % 2 == 1){
            B[i+1]++;
            res+=2;
        }
    }
    return B[B.size() - 1] % 2 == 0 ? to_string(res) : "NO";
}