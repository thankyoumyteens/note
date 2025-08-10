# 获取月份的第一天和最后一天

```java
LocalDate date = LocalDate.now();
// 获取本月的第一天
LocalDate firstDay = date.with(TemporalAdjusters.firstDayOfMonth());
// 获取本月的最后一天
LocalDate lastDay = date.with(TemporalAdjusters.lastDayOfMonth());
```
