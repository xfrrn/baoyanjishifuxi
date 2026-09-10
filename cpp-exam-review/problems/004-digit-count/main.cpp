#include<iostream>
#include<string>

using namespace std;
int main(){
    int n;
    cin>>n;
    cin.get();

    for(int o=0;o<n;o++){
        string line;
        getline(cin,line);
        int num=line.size();
        int num_size=0;
        for(int oo=0;oo<num;oo++){

            if(line[oo]=='0'){num_size++;}
            if(line[oo]=='1'){num_size++;}
            if(line[oo]=='2'){num_size++;}
            if(line[oo]=='3'){num_size++;}
            if(line[oo]=='4'){num_size++;}
            if(line[oo]=='5'){num_size++;}
            if(line[oo]=='6'){num_size++;}
            if(line[oo]=='7'){num_size++;}
            if(line[oo]=='8'){num_size++;}
            if(line[oo]=='9'){num_size++;}
            
        }
        cout<<num_size<<'\n';
    }
}