# 字符串转日期和时间

```cpp
#include <iostream>
#include <chrono>
#include <ctime>
#include <string>
#include <sstream>
#include <iomanip>

// 格式化输出时间点
std::string format_time(const std::chrono::time_point<std::chrono::system_clock> &tp) {
    std::time_t tt = std::chrono::system_clock::to_time_t(tp);
    char buffer[100];
    std::strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", std::localtime(&tt));
    return buffer;
}

// 将字符串转换为system_clock::time_point
std::chrono::time_point<std::chrono::system_clock> string_to_timepoint(
        const std::string &time_str,
        const std::string &format = "%Y-%m-%d %H:%M:%S"
) {
    std::tm tm = {};
    std::istringstream ss(time_str);

    // 按照指定格式解析字符串到tm结构体
    ss >> std::get_time(&tm, format.c_str());

    if (ss.fail()) {
        throw std::invalid_argument("无效的时间字符串格式: " + time_str);
    }

    // 转换为time_t，再转换为system_clock::time_point
    std::time_t tt = std::mktime(&tm);
    return std::chrono::system_clock::from_time_t(tt);
}

int main() {
    std::string str1 = "2023-10-01 15:30:45";
    std::chrono::time_point<std::chrono::system_clock> tp1 = string_to_timepoint(str1);
    std::cout << "原始字符串: " << str1 << "\n转换后: " << format_time(tp1) << "\n\n";
    return 0;
}
```
