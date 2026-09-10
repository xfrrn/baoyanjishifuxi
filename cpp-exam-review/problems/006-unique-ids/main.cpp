#include<iostream>
#include<algorithm>
using namespace std;

int main(){
    int n;
    cin>>n;
    int number[1000];
    for(int i=0;i<n;i++){
        cin>>number[i];
    }
    sort(number,number+n);

    int diff=0;
    int diffs[1000];

    for(int i=0;i<n;){
        while(number[i]==number[i+1]){
            i++;
        }
        
        diffs[diff]=number[i];
        diff++;
        i++;

    }
    cout<<diff<<'\n';
    for(int i=0;i<diff;i++){
        cout<<diffs[i]<<' ';
    }
}