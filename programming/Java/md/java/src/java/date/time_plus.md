# 时间加减

```java
LocalTime time = LocalTime.now();

// 加1小时
LocalTime plusHours = time.plusHours(1L);
// 减1小时
LocalTime minusHours = time.minusHours(1L);

// 加1分钟
LocalTime plusMinutes = time.plusMinutes(1L);
// 减1分钟
LocalTime minusMinutes = time.minusMinutes(1L);

// 加1秒
LocalTime plusSeconds = time.plusSeconds(1L);
// 减1秒
LocalTime minusSeconds = time.minusSeconds(1L);

// 加1纳秒
LocalTime plusNanos = time.plusNanos(1L);
// 减1纳秒
LocalTime minusNanos = time.minusNanos(1L);
```
