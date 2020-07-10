# 引入头文件

```cpp
#include <string>
using std::string;
```

# 拷贝初始化

使用"="执行的是拷贝初始化

```cpp
// 拷贝初始化
string s1 = "abc";
// 直接初始化
string s2("bcd");
```

# 读写string对象

```cpp
string s1, s2;
// 输入输出操作返回
// 运算符左侧的对象
// 所以可以连写
cin >> s1 >> s2;
cout << s << endl;
```
在读取时,string对象会忽略开头的空白(空格,换行等),并从第一个真正的字符开始读取，直到遇见下一处空白

# getline()

定义
```cpp
getline(inputStream, stringObject);
```

getline从参数1输入流中读取,直到遇到换行符(注意:换行符也被读入),
然后它把读入的内容存到参数2中(注意:不包括换行符)

getline执行完会返回参数1的流对象

# empty()和size()

```cpp
// 返回字符串是否为空
bool b = s.empty();
// 返回字符串中的字符个数
string::size_type sz = s.size();
```
string::size_type 是一个无符号整数

# string的比较

使用">","<","!="等运算符,默认按照字典顺序比较



