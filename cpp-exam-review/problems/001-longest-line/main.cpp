#include <iostream>
using namespace std;

int main(){
    int n;  //行数
    cin>>n;
    
    int u=0,i1=0; // 第几行和几个数字

    string line;

    for(int i=0;i<n;i++){
        getline(string,line);
        int s = string.size(string);
        if(s>i1){
            i1=s;
            u=i;
        }
    }
    cout<<u<<" "<<i1;

}