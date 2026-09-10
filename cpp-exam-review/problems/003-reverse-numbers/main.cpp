/* 你的原始写法（已通过全部 14 组测试，保留供对照）
#include<iostream>
using namespace std;
int main(){
    int number;
    cin>>number;
    int zhengshu[number];
    for(int oo=0;oo<number;oo++){
        cin>>zhengshu[oo];
    }
    number--;
    while(number!=-1){
        cout<<zhengshu[number];
        number--;
        if(number!=-1){cout<<" ";}
    }
}
*/

// 参考写法：仍然是先存入数组，再从后往前输出。
#include <iostream>
using namespace std;

int main() {
    int n;
    cin >> n;  // n 表示一共有多少个整数，后面不改变它

    // 题目最多有 1000 个数，准备 1000 个位置就够了。
    // 数组下标从 0 开始，这个数组的合法下标为 0 到 999。
    int a[1000];

    // 输入 n 个整数，依次存入 a[0]、a[1]、……、a[n - 1]。
    // cin >> 读取整数时会自动跳过空格和换行，不需要 cin.get()。
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    // 最后一个数的下标是 n - 1，先输出它。
    // i-- 表示每次向前移动一个位置，一直输出到 a[0]。
    // 当 i 变成 -1 时，i >= 0 不成立，循环结束。
    for (int i = n - 1; i >= 0; i--) {
        cout << a[i];

        // i > 0 说明后面还有数要输出，因此加一个分隔空格。
        // i == 0 时输出的是最后一个数，后面不再加空格。
        if (i > 0) {
            cout << " ";
        }
    }

    cout << '\n';  // 所有数字输出完后换行
    return 0;
}
