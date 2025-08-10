# 初始化日期和时间

```java
// 年月日
LocalDate date = LocalDate.of(2021, 2, 26);
// 时分秒
LocalTime time = LocalTime.of(15, 37, 4);
// 年月日 时分秒
LocalDateTime dateTime = LocalDateTime.of(2021, 2, 26, 15, 37, 4);
// 年月日 时分秒 纳秒
// 纳秒的取值范围: 0 到 999,999,999
LocalDateTime dateTime = LocalDateTime.of(2021, 2, 26, 15, 37, 4, 9999);
```
