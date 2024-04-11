# 日期操作

LocalDate 和 LocalTime 分别表示日期和时间, LocalDateTime 表示日期和时间。它们是不可变的对象, 可以进行操作, 但不能修改它们。

## 获取当前日期和时间

```java
// 2021-02-26
LocalDate now = LocalDate.now();
// 15:37:04.556
LocalTime now = LocalTime.now();
// 2021-02-26T15:37:04.556
LocalDateTime now = LocalDateTime.now();
```

## 初始化日期和时间

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

## 修改日期和时间

```java
LocalDateTime dateTime = LocalDateTime.now();

lastDay.withYear(2000);
lastDay.withMonth(1);
lastDay.withDayOfMonth(1);
dateTime = dateTime.withHour(23);
dateTime = dateTime.withMinute(59);
dateTime = dateTime.withSecond(59);
```

## 字符串转日期和时间

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

## 日期和时间转字符串

```java
// 年月日
DateTimeFormatter dateFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
String dateStr = date.format(dateFormatter);
// 时分秒
DateTimeFormatter timeFormatter = DateTimeFormatter.ofPattern("HH:mm:ss");
String timeStr = time.format(timeFormatter);
// 年月日 时分秒
DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
String dateTimeStr = dateTime.format(dateTimeFormatter);
```

## 日期加减

```java
LocalDate date = LocalDate.now();

// 加1天
LocalDate plusDays = date.plusDays(1L);
// 减1天
LocalDate minusDays = date.minusDays(1L);

// 加1月
LocalDate plusMonths = date.plusMonths(1L);
// 减1月
LocalDate minusMonths = date.minusMonths(1L);

// 加1年
LocalDate plusYears = date.plusYears(1L);
// 减1年
LocalDate minusYears = date.minusYears(1L);

// 加1周
LocalDate plusWeeks = date.plusWeeks(1L);
// 减1周
LocalDate minusWeeks = date.minusWeeks(1L);
```

## 时间加减

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

## 日期和时间加减

LocalDateTime 包含上面日期加减和时间加减的方法。

## 日期和时间比较

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

## 两个日期的间隔

```java
LocalDate now = LocalDate.now();

long duration = now.until(date, ChronoUnit.DAYS);
```

## 两个时间的间隔

```java
LocalTime now = LocalTime.now();

long duration = now.until(date, ChronoUnit.SECONDS);
```

## 获取月份的第一天和最后一天

```java
LocalDate date = LocalDate.now();
// 获取本月的第一天
LocalDate firstDay = date.with(TemporalAdjusters.firstDayOfMonth());
// 获取本月的最后一天
LocalDate lastDay = date.with(TemporalAdjusters.lastDayOfMonth());
```

## LocalDateTime 转 Date

```java
LocalDateTime now = LocalDateTime.now();

ZoneId zoneId = ZoneId.systemDefault();
ZonedDateTime zdt = now.atZone(zoneId);

Date date = Date.from(zdt.toInstant());
```

## Date 转 LocalDateTime

```java
Date date = new Date();

Instant instant = date.toInstant();
ZoneId zoneId = ZoneId.systemDefault();
ZonedDateTime zdt = instant.atZone(zoneId);

LocalDateTime localDateTime = zdt.toLocalDateTime();
```
