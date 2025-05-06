long long candies(unsigned n, vector<unsigned> arr) {
    vector<unsigned> candies(arr.size(), 1);
    
    for(unsigned i = 1; i < n; i++)
        if(arr[i] > arr[i-1])
            candies[i] = candies[i-1] + 1;
    
    for(int i = n - 2; i >= 0 ; i--)
        if(arr[i] > arr[i + 1])
            candies[i] = max(candies[i + 1] + 1, candies[i]);

    return accumulate(candies.begin(), candies.end(), static_cast<long long>(0));   
}