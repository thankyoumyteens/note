# 实现 Runnable

实现 Runnable 接口, 实现 run 方法

```java
public class Tester {
    public static class MyThread implements Runnable {
        @Override
        public void run() {
            System.out.println("Thread: " + Thread.currentThread().getName() + " is running");
        }
    }

    public static void main(String[] args) {
        Thread t1 = new Thread(new MyThread());
        t1.start();
    }
}
```
