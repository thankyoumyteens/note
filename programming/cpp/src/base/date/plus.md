# 日期加减

```cpp
#include <iostream>
#include <chrono>
#include <ctime>
#include <stdexcept>

// 日期加减函数
template<typename Duration>
std::chrono::time_point<std::chrono::system_clock> add_time(const std::chrono::time_point<std::chrono::system_clock> &tp,
                                          Duration duration) {
    return tp + duration;
}

template<typename Duration>
std::chrono::time_point<std::chrono::system_clock> subtract_time(const std::chrono::time_point<std::chrono::system_clock> &tp,
                                               Duration duration) {
    return tp - duration;
}

int main() {
    try {
        // 创建一个基准日期：2023年3月15日 10:30:00
        auto base_date = create_datetime(2023, 3, 15, 10, 30, 0);

        auto add_1_day = add_time(base_date, std::chrono::hours(24));
        std::cout << "加1天: " << format_time(add_1_day) << std::endl;

        auto add_2_weeks = add_time(base_date, std::chrono::hours(2 * 7 * 24));
        std::cout << "加2周: " << format_time(add_2_weeks) << std::endl;

        auto add_30_minutes = add_time(base_date, std::chrono::minutes(30));
        std::cout << "加30分钟: " << format_time(add_30_minutes) << std::endl;

        auto add_complex = add_time(base_date, std::chrono::hours(3 * 24) + std::chrono::minutes(45));
        std::cout << "加3天45分钟: " << format_time(add_complex) << std::endl << std::endl;

        auto subtract_1_month = subtract_time(base_date, std::chrono::hours(30 * 24)); // 近似1个月
        std::cout << "减30天(近似1个月): " << format_time(subtract_1_month) << std::endl;

        auto subtract_2_hours = subtract_time(base_date, std::chrono::hours(2));
        std::cout << "减2小时: " << format_time(subtract_2_hours) << std::endl;

        auto subtract_5_seconds = subtract_time(base_date, std::chrono::seconds(5));
        std::cout << "减5秒: " << format_time(subtract_5_seconds) << std::endl << std::endl;
    }
    catch (const std::exception &e) {
        std::cerr << "错误: " << e.what() << std::endl;
        return 1;
    }
    return 0;
}
```
