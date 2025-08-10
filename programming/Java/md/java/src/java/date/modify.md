# 修改日期和时间

```java
LocalDateTime dateTime = LocalDateTime.now();

// 修改年
dateTime = dateTime.withYear(2000);
// 修改月
dateTime = dateTime.withMonth(1);
// 修改日
dateTime = dateTime.withDayOfMonth(1);

// 修改时
dateTime = dateTime.withHour(23);
// 修改分
dateTime = dateTime.withMinute(59);
// 修改秒
dateTime = dateTime.withSecond(59);
```
