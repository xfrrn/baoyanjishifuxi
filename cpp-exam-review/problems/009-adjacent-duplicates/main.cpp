#include<iostream>
using namespace std;

int main(){
    string line;
    getline(cin,line);

    char first = line[0];

    for(char Ch:line){
       if(first!=Ch){
        cout<<first;
       }
       first=Ch;
    }
    cout<<first;
}