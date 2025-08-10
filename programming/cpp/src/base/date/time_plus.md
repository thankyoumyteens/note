# 时间加减

```cpp
int main() {
    try {
        // 创建基准时间点：2023-10-01 15:30:45.500
        auto base_time = create_time(2023, 10, 1, 15, 30, 45, 500);

        auto add_hours = base_time + chr::hours(2);          // 加2小时
        auto add_minutes = base_time + chr::minutes(45);     // 加45分钟
        auto add_seconds = base_time + chr::seconds(30);     // 加30秒
        auto add_ms = base_time + chr::milliseconds(250);    // 加250毫秒
        auto add_complex = base_time + chr::hours(1) + chr::minutes(30) + chr::seconds(15); // 复杂组合

        auto sub_hours = base_time - chr::hours(1);          // 减1小时
        auto sub_minutes = base_time - chr::minutes(20);     // 减20分钟
        auto sub_seconds = base_time - chr::seconds(10);     // 减10秒
        auto sub_ms = base_time - chr::milliseconds(300);    // 减300毫秒

    } catch (const std::exception &e) {
        std::cerr << "错误: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
```
