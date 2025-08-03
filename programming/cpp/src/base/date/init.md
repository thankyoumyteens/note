# 初始化日期和时间

```cpp
#include <iostream>
#include <chrono>
#include <ctime>

// 将指定的日期时间转换为system_clock时间点
std::chrono::time_point<std::chrono::system_clock> create_datetime(
        int year, int month, int day,
        int hour = 0, int minute = 0, int second = 0
) {

    // 初始化tm结构体
    std::tm tm_time = {};  // 初始化所有成员为0
    tm_time.tm_year = year - 1900;  // 年份从1900开始计算
    tm_time.tm_mon = month - 1;     // 月份范围0-11
    tm_time.tm_mday = day;
    tm_time.tm_hour = hour;
    tm_time.tm_min = minute;
    tm_time.tm_sec = second;

    // 转换为time_t
    std::time_t tt = std::mktime(&tm_time);

    // 转换为system_clock时间点
    return std::chrono::system_clock::from_time_t(tt);
}

int main() {
    // 2020年12月31日 23:59:59
    std::chrono::time_point<std::chrono::system_clock> date = create_datetime(2020, 12, 31, 23, 59, 59);
    std::cout << "Formatted time: " << format_time(date) << std::endl;
    return 0;
}
```