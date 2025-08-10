# 字符串转日期和时间

```java
// 年月日
DateTimeFormatter dateFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
LocalDate date = LocalDate.parse("2021-02-26", dateFormatter);

// 时分秒
DateTimeFormatter timeFormatter = DateTimeFormatter.ofPattern("HH:mm:ss");
LocalTime time = LocalTime.parse("15:37:04", timeFormatter);

// 年月日 时分秒
DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
LocalDateTime dateTime = LocalDateTime.parse("2021-02-26 15:37:04", dateTimeFormatter);
```
