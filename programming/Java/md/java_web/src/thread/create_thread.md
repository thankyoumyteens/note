# 创建线程的方式

1. 继承 Thread
2. 实现 Runnable
3. 实现 Callable
4. 使用线程池

## Runnable 和 Callable 的区别

1. Runnable 的 run 方法没有返回值。Callable 的 call 方法有返回值, 可以搭配 FutureTask 获取返回值
2. Runnable 的 run 方法不允许向外抛出异常。Callable 的 call 方法可以向外抛出异常

## run 方法和 start 方法的区别

1. run 方法不会启动线程。start 方法用来启动线程
2. run 方法是线程要执行的代码, 可以被调用多次。start 方法一个线程只能被调用一次

## 继承 Thread

```java
public static void main(String[] args) {
    new Thread() {
        @Override
        public void run() {
            System.out.println("Hello, world!");
        }
    }.start();
}
```

## 实现 Runnable

```java
public static void main(String[] args) {
    Runnable runnable = new Runnable() {
        @Override
        public void run() {
            System.out.println("Hello, world!");
        }
    };
    new Thread(runnable).start();
}
```

## 实现 Callable

```java
public static void main(String[] args) {
    Callable<String> callable = new Callable<>() {
        @Override
        public String call() throws Exception {
            return "Hello, world!";
        }
    };
    FutureTask<String> futureTask = new FutureTask<>(callable);
    new Thread(futureTask).start();
    try {
        // get() 方法会等待线程执行完成, 并获取返回值
        System.out.println(futureTask.get());
    } catch (Exception e) {
        e.printStackTrace();
    }
}
```

## 使用线程池

```java
public static void main(String[] args) {
    ExecutorService executorService = Executors.newFixedThreadPool(3);
    executorService.submit(() -> System.out.println("Runnable"));
    executorService.shutdown();
}
```
