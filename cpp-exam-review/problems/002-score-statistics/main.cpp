#include<iostream>
using namespace std;

int main(){
    int n,k;
    cin>>n;
    cin.get();
    cin>>k;
    cin.get();

    int all_score=0;
    int dabiao=0;

    for(int s=0;s<n;s++){
        int score;
        cin>>score;
        if(score>=k){
            all_score+=score;
            dabiao+=1;
        }
    }
    
    cout<<dabiao<<" "<<all_score;
    
}