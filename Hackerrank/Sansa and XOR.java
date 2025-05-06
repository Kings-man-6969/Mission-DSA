public static int sansaXor(List<Integer> arr) {
    int n = arr.size();
        int c = 0;

       
        if (n % 2 == 0) {
            return 0;
        }
       
        for (int i = 0; i < n; i += 2) {
            c ^= arr.get(i);
        }

        return c;

    }