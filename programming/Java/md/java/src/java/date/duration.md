# 两个日期和时间的间隔

```java
LocalDate date = LocalDate.now();
LocalTime time = LocalTime.now();

long duration = date.until(date1, ChronoUnit.DAYS);

long duration = time.until(time1, ChronoUnit.SECONDS);
```
