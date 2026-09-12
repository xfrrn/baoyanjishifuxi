/* 原提交（完整保留）
#include<iostream>

using namespace std;

int main()
{
    int n;
    cin>>n;

    int number[1001]={0};

    int s;

    for(int i=0;i<n;i++)
    {   
        cin>>s;
        number[s]++;

    }

    int out1,out2;

    out1=0;
    out2=number[0];
    for(int i=1;i<1000;i++)
    {   


        if(number[i]>out2)
        {
            out1=i;
            out2=number[i];
        }
    }

    cout<<out1<<' '<<out2;
}
*/

// 参考实现
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;

    int number[1001] = {0};
    for (int i = 0; i < n; ++i) {
        int id;
        cin >> id;
        ++number[id];
    }

    int answer = 1;
    // 从小到大扫描，仅在次数更多时更新，保证并列时编号最小。
    for (int id = 2; id <= 1000; ++id) {
        if (number[id] > number[answer]) {
            answer = id;
        }
    }
    cout << answer << ' ' << number[answer] << '\n';
    return 0;
}
