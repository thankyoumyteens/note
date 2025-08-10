# 日期和时间加减

```java
LocalDateTime now = LocalDateTime.now();

// 加1天
LocalDateTime plusDays = now.plusDays(1L);
// 减1天
LocalDateTime minusDays = now.minusDays(1L);

// 加1月
LocalDateTime plusMonths = now.plusMonths(1L);
// 减1月
LocalDateTime minusMonths = now.minusMonths(1L);

// 加1年
LocalDateTime plusYears = now.plusYears(1L);
// 减1年
LocalDateTime minusYears = now.minusYears(1L);

// 加1周
LocalDateTime plusWeeks = now.plusWeeks(1L);
// 减1周
LocalDateTime minusWeeks = now.minusWeeks(1L);

// 加1小时
LocalDateTime plusHours = now.plusHours(1L);
// 减1小时
LocalDateTime minusHours = now.minusHours(1L);

// 加1分钟
LocalDateTime plusMinutes = now.plusMinutes(1L);
// 减1分钟
LocalDateTime minusMinutes = now.minusMinutes(1L);

// 加1秒
LocalDateTime plusSeconds = now.plusSeconds(1L);
// 减1秒
LocalDateTime minusSeconds = now.minusSeconds(1L);

// 加1纳秒
LocalDateTime plusNanos = now.plusNanos(1L);
// 减1纳秒
LocalDateTime minusNanos = now.minusNanos(1L);
```
