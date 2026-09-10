#include<iostream>

using namespace std;

int main(){
    int n,m;
    cin>>n>>m;
    int op[1000][2];

    int falses=0;

    for(int i=0;i<n;i++){
        cin>>op[i][0];
        cin>>op[i][1];
    }

    for(int i=0;i<n;i++){
        if(op[i][0]==1){
            m+=op[i][1];
        }
         if(op[i][0]==2){
            if(m>=op[i][1]){
            m-=op[i][1];}
            else{
                falses++;
            }
        }


    }
    cout<<m<<' '<<falses;

}