# 保证线程的执行顺序

```java
public static void main(String[] args) {
    Thread t1 = new Thread(() -> {
        System.out.println("1");
    });
    Thread t2 = new Thread(() -> {
        System.out.println("2");
    });
    Thread t3 = new Thread(() -> {
        System.out.println("3");
    });

    t1.start();
    t2.start();
    t3.start();
}
```

## 使用 join 方法

```java
public static void main(String[] args) {
    Thread t1 = new Thread(() -> {
        System.out.println("1");
    });
    Thread t2 = new Thread(() -> {
        try {
            // join 方法会阻塞当前线程, 直到t1线程执行完毕
            t1.join();
        } catch (InterruptedException ignored) {
        }
        System.out.println("2");
    });
    Thread t3 = new Thread(() -> {
        try {
            // join 方法会阻塞当前线程, 直到t2线程执行完毕
            t2.join();
        } catch (InterruptedException ignored) {
        }
        System.out.println("3");
    });

    t1.start();
    t2.start();
    t3.start();
}
```
