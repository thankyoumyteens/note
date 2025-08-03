# 修改日期和时间

```cpp
#include <iostream>
#include <chrono>
#include <ctime>

// 格式化输出时间点
std::string format_time(const std::chrono::time_point<std::chrono::system_clock> &tp) {
    std::time_t tt = std::chrono::system_clock::to_time_t(tp);
    char buffer[100];
    std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", std::localtime(&tt));
    return buffer;
}

// 将时间点转换为tm结构体
std::tm time_point_to_tm(const std::chrono::time_point<std::chrono::system_clock> &tp) {
    std::time_t tt = std::chrono::system_clock::to_time_t(tp);
    return *std::localtime(&tt); // 返回本地时间结构体
}

// 将tm结构体转换为时间点
std::chrono::time_point<std::chrono::system_clock> tm_to_time_point(const std::tm &tm) {
    std::time_t tt = std::mktime(const_cast<std::tm *>(&tm));
    return std::chrono::system_clock::from_time_t(tt);
}

int main() {
    // 获取当前系统时间点
    std::chrono::time_point<std::chrono::system_clock> now = std::chrono::system_clock::now();
    std::cout << "当前时间: " << format_time(now) << std::endl;

    std::tm tm = time_point_to_tm(now);
    // 修改年份为2025
    tm.tm_year = 2025 - 1900; // 注意年份计算方式
    std::chrono::time_point<std::chrono::system_clock> modified_year = tm_to_time_point(tm);
    std::cout << "修改年份后: " << format_time(modified_year) << std::endl;

    // 修改月份为6月（6-1=5）
    tm = time_point_to_tm(now); // 重置为当前时间
    tm.tm_mon = 5; // 0表示1月，5表示6月
    std::chrono::time_point<std::chrono::system_clock> modified_month = tm_to_time_point(tm);
    std::cout << "修改月份后: " << format_time(modified_month) << std::endl;

    // 修改日期为15日
    tm = time_point_to_tm(now);
    tm.tm_mday = 15;
    std::chrono::time_point<std::chrono::system_clock> modified_day = tm_to_time_point(tm);
    std::cout << "修改日期后: " << format_time(modified_day) << std::endl;

    // 修改时间为18:30
    tm = time_point_to_tm(now);
    tm.tm_hour = 18;
    tm.tm_min = 30;
    tm.tm_sec = 0;
    std::chrono::time_point<std::chrono::system_clock> modified_time = tm_to_time_point(tm);
    std::cout << "修改时间后: " << format_time(modified_time) << std::endl;
    return 0;
}
```
