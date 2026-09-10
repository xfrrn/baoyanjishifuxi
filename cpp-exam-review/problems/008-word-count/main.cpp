/*
你的原提交（完整保留）：

#include<iostream>
using namespace std;
int main()
{
    string line;
    getline(cin,line);
    int n=line.size();
    int s=0;

    for(int i=0;i<n;)
    {
        int opp=0;
        while(line[i]!=' '){
            i++;
            opp=1;
        }
        while(line[i]==' '){
            i++;
        }
        if(opp==1){s++;}
    }
    cout<<s;
}
*/

#include <iostream>
#include <string>
using namespace std;

int main() {
    string line;
    getline(cin, line);

    int wordCount = 0;
    bool inWord = false;  // 当前是否处在一段连续字母中

    for (char ch : line) {
        if (ch != ' ') {
            // 从空格进入字母时，说明遇到了一个新单词。
            if (!inWord) {
                wordCount++;
                inWord = true;
            }
        } else {
            // 遇到空格后，当前单词结束。
            inWord = false;
        }
    }

    cout << wordCount << '\n';
    return 0;
}
