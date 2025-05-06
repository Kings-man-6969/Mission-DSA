vector<double> runningMedian(vector<int> const&a) {
    if(0==a.size())
        return vector<double>();
    map<int,int> aux; 
    aux.insert({a[0],1});
    auto lowerMed = aux.begin();
    vector<double> retq;
    retq.push_back(1.0*(lowerMed->first));
    int pos=0;
    for(int i=1; i<a.size();i++)
    {
        if(!aux.count(a[i]))
            aux.insert({a[i],1});
        else{aux[a[i]]++;}
        if((a[i]<lowerMed->first)&&(i&1))
            pos--;
        else if((a[i]>=lowerMed->first)&&(0==(i&1)))
            pos++;
        if(0>pos)
        {
            lowerMed--;
            pos=lowerMed->second-1;
        }
        else if(lowerMed->second<=pos)
        {
            lowerMed++;
            pos=0;
        }
        if(0==(i&1))
        {
            retq.push_back(1.0*(lowerMed->first));
        }
        else
        {
            auto x=lowerMed;
            if(pos+1>=lowerMed->second)
                x++; 
            retq.push_back(0.5*(lowerMed->first + x->first));
        }
    }
    return retq;
}