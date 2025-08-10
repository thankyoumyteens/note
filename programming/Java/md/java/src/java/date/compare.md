# 日期和时间比较

```java
LocalDate date = LocalDate.now();
LocalTime time = LocalTime.now();
LocalDateTime now = LocalDateTime.now();

// 判断 date 是否在参数的日期之前
boolean dateBefore = date.isBefore(date.plusDays(1L));
// 判断 time 是否在参数的时间之前
boolean timeBefore = time.isBefore(time.plusSeconds(1L));
// 判断 now 是否在参数的日期时间之前
boolean before = now.isBefore(now.plusHours(1L));

// 判断 date 是否在参数的日期之后
boolean dateAfter = date.isAfter(date.plusDays(1L));
// 判断 time 是否在参数的时间之后
boolean timeAfter = time.isAfter(time.plusSeconds(1L));
// 判断 now 是否在参数的日期时间之后
boolean after = now.isAfter(now.plusHours(1L));

// 判断 date 和参数的日期是否相等
boolean dateEqual = date.isEqual(date.plusDays(1L));
// 时间没有isEqual方法
// 判断 now 和参数的日期时间是否相等
boolean equal = now.isEqual(now.plusHours(1L));
```
