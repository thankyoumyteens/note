# 继承 Thread

继承 Thread 类, 重写 run 方法

```java
public class Tester {
    public static class MyThread extends Thread {
        @Override
        public void run() {
            System.out.println("Thread: " + Thread.currentThread().getName() + " is running");
        }
    }

    public static void main(String[] args) {
        MyThread t1 = new MyThread();
        t1.start();
    }
}
```
