#include<iostream>
using namespace std;

int main()
{
    int n;
    cin >>n;

    int number[1000];
    int output[1000];
    for(int i=0;i<n;i++)
    {
        cin>>number[i];
    }
    for(int i=0;i<n;i++)
    {   int one;
        output[i]=0;
        while(number[i]!=0){
            one=number[i]%10;
            number[i]=(number[i]-one)/10;
            output[i]+=one;
        }
    }
    for(int i=0;i<n;i++){
        cout<<output[i]<<'\n';
    }
}