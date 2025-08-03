# 获取当前日期和时间

```cpp
#include <iostream>
#include <chrono>   // 用于获取时间点
#include <ctime>    // 用于时间转换和格式化

// 获取当前日期和时间，返回结构体
std::tm *get_current_datetime() {

    // 1. 获取当前系统时间点
    std::chrono::time_point<std::chrono::system_clock> now = std::chrono::system_clock::now();

    // 2. 转换为time_t类型
    std::time_t current_time = std::chrono::system_clock::to_time_t(now);

    // 3. 转换为本地时间结构
    std::tm *local_tm = std::localtime(&current_time);

    return local_tm;
}

int main() {
    std::tm *now = get_current_datetime();
    // tm_year是从1900年开始的计数
    std::cout << "年：" << now->tm_year + 1900 << "\n";
    // tm_mon范围是0-11，需要加1
    std::cout << "月：" << now->tm_mon + 1 << "\n";
    std::cout << "日：" << now->tm_mday << "\n";
    std::cout << "时：" << now->tm_hour << "\n";
    std::cout << "分：" << now->tm_min << "\n";
    std::cout << "秒：" << now->tm_sec << "\n";
    return 0;
}
```
