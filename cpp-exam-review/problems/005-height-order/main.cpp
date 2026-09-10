#include<iostream>
#include<algorithm>
using namespace std;

int main()
{
    int n;
    int hig[1000];
    cin>>n;
    for(int s=0;s<n;s++){
        cin>>hig[s];
    }
    sort(hig,hig+n);
    for(int s=0;s<n;s++){
        cout<<hig[s];
        if(s!=n-1){
            cout<<' ';
        }
    }
}