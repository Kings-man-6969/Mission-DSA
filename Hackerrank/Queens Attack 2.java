import java.io.*;
import java.util.*;

public class Solution {

    static int queensAttack(int n, int k, int r, int c, int[][] obstacles) {
        Set<String> obs = new HashSet<>();
        for (int[] ob : obstacles) obs.add(ob[0] + "," + ob[1]);
        int count = 0;
        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}, {1, 1}, {-1, -1}, {1, -1}, {-1, 1}};
        for (int[] dir : dirs) {
            for (int i = 1; ; i++) {
                int nr = r + dir[0] * i, nc = c + dir[1] * i;
                if (nr < 1 || nr > n || nc < 1 || nc > n || obs.contains(nr + "," + nc)) break;
                count++;
            }
        }
        return count;
    }

    public static void main(String[] args) throws IOException {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt(), k = sc.nextInt();
        int r = sc.nextInt(), c = sc.nextInt();
        int[][] obstacles = new int[k][2];
        for (int i = 0; i < k; i++) {
            obstacles[i][0] = sc.nextInt();
            obstacles[i][1] = sc.nextInt();
        }
        System.out.println(queensAttack(n, k, r, c, obstacles));
    }
}