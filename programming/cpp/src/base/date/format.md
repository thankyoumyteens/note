# 日期格式化

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

int main() {
    auto now = std::chrono::system_clock::now();
    std::cout << "Formatted time: " << format_time(now) << std::endl;
    return 0;
}
```
