# 停止一个正在运行的线程

## 循环检查标志位

```java
public static class MyThread extends Thread {
    public boolean isRunning = true;

    @Override
    public void run() {
        while (isRunning) {
            System.out.println("Thread is running");
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}

public static void main(String[] args) {
    MyThread t1 = new MyThread();
    t1.start();
    try {
        Thread.sleep(5000);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    t1.isRunning = false;

}
```

## 调用 interrupt 中断线程

1. 线程阻塞时调用会抛出 InterruptedException

```java
public static class MyThread extends Thread {
    @Override
    public void run() {
        while (true) {
            System.out.println("Thread is running");
            try {
                Thread.sleep(5000);
            } catch (InterruptedException e) {
                System.out.println("Thread is interrupted");
                return;
            }
        }
    }
}

public static void main(String[] args) {
    MyThread t1 = new MyThread();
    t1.start();
    try {
        Thread.sleep(1000);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    t1.interrupt();
}
```

2. 线程不阻塞时调用可以当标志位使用

```java
public static class MyThread extends Thread {
    @Override
    public void run() {
        while (true) {
            System.out.println("Thread is running");
            if (Thread.interrupted()) {
                System.out.println("Thread is interrupted");
                break;
            }
        }
    }
}

public static void main(String[] args) {
    MyThread t1 = new MyThread();
    t1.start();
    try {
        Thread.sleep(1000);
    } catch (InterruptedException e) {
        e.printStackTrace();
    }
    t1.interrupt();
}
```
