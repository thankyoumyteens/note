# 获取当前日期和时间

```java
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.LocalDateTime;

public class Main {
    public static void main(String[] args) {
        // 2021-02-26
        LocalDate now = LocalDate.now();
        // 15:37:04.556
        LocalTime now = LocalTime.now();
        // 2021-02-26 15:37:04.556
        LocalDateTime now = LocalDateTime.now();
    }
}
```
