/* 原始代码（保留供对照）
#include <iostream>
#include<string>
using namespace std;

int main(){
    int n;  //行数
    cin>>n;
    
    int u=0,i1=0; // 第几行和几个数字

    string line;

    for(int i=0;i<n;i++){
        getline(cin,line);
        int s = line.size();
        if(s>i1){
            i1=s;
            u=i;
        }
    }
    cout<<u<<" "<<i1;

}
*/

#include <iostream>
#include <string>
using namespace std;

int main() {
    int n;
    cin >> n;
    cin.get();  // 读走 n 后面的一个换行符

    int bestLine = 1;
    int maxLength = -1;  // 第一行即使为空，也能成为初始答案。
    string line;

    for (int i = 1; i <= n; i++) {
        getline(cin, line);
        int length = line.size();  // 这一行的字符数，空格也算
        // 只在更长时更新，长度相同则保留较早的行。
        if (length > maxLength) {
            maxLength = length;
            bestLine = i;
        }
    }

    cout << bestLine << " " << maxLength << '\n';
    return 0;
}
