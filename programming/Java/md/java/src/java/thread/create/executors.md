# Executors

```java
import java.util.concurrent.*;

public class Tester {

    public static void main(String[] args) {
        try (ExecutorService executorService = Executors.newFixedThreadPool(1)) {
            executorService.execute(new Runnable() {
                @Override
                public void run() {
                    System.out.println("Hello World");
                }
            });
        }
    }
}
```
