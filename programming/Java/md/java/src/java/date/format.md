# 日期和时间转字符串

```java
// 年月日
LocalDate date = LocalDate.now();
DateTimeFormatter dateFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
String dateStr = date.format(dateFormatter);

// 时分秒
LocalTime time = LocalTime.now();
DateTimeFormatter timeFormatter = DateTimeFormatter.ofPattern("HH:mm:ss");
String timeStr = time.format(timeFormatter);

// 年月日 时分秒
LocalDateTime dateTime = LocalDateTime.now();
DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
String dateTimeStr = dateTime.format(dateTimeFormatter);
```
