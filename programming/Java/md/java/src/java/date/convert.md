# LocalDateTime 和 Date 互转

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
