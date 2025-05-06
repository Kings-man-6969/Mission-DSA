char* highestValuePalindrome(char* s, int n, int k) {
    int l = 0 , h = n-1;
    char* ret = (char*)malloc(n+1);
    int num_invaild = count_invaild_chars(s, n+1);
    int extra = k-num_invaild;
    ret[n] = '\0';
    printf("invaild = %d\n" , num_invaild);
    if(num_invaild> k)
        return "-1";
    else
    {
        
        for(; l <=h ; l++ , h--)
        {
            if(s[l] != s[h] && (s[l] == '9' || s[h] =='9'))
            {
                k--;
                num_invaild--;
                if(s[l] >= s[h])
                {
                    ret[l] = s[l];
                    ret[h] = s[l];
                }
                else
                {
                    ret[l] = s[h];
                    ret[h] = s[h];
                }
            }
            else if(s[l] != s[h] && (s[l] != '9' && s[h] !='9'))
            {
                
                if(extra >= 1)
                {
                    extra--;
                    k-=2;
                    num_invaild--;
                    ret[l] ='9';
                    ret[h] ='9';
                }
                else
                {
                    k--;
                    num_invaild--;
                    if(s[l] >= s[h])
                    {
                        ret[l] = s[l];
                        ret[h] = s[l];
                    }
                    else
                    {
                        ret[l] = s[h];
                        ret[h] = s[h];
                    }
                }
            }
            else if (s[l] == s[h] && extra >= 2 && s[l] != '9')
            {
                extra-=2;
                k-=2;
                ret[l] = '9';
                ret[h] = '9';
            }
            else
            {
                ret[l] = s[l];
                ret[h] = s[h];
            }
        }
    }
    if(n%2 != 0 && k >0)
    {
        ret[(n/2)] = '9';
    }
    
    return ret;     
}