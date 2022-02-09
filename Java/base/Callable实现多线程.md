# Callable

Callable位于java.util.concurrent包下

```java
public interface Callable<V> {
    /**
     * Computes a result, or throws an exception if unable to do so.
     *
     * @return computed result
     * @throws Exception if unable to compute a result
     */
    V call() throws Exception;
}
```

一般情况下是配合ExecutorService来使用的，在ExecutorService接口中声明了若干个submit方法的重载版本

```java
<T> Future<T> submit(Callable<T> task);
<T> Future<T> submit(Runnable task, T result);
Future<?> submit(Runnable task);
```

# Future

Future类位于java.util.concurrent包下，对具体的Runnable或者Callable任务的执行结果进行取消、查询是否完成、获取结果。

```java
public interface Future<V> {
    /**
     * 取消任务，如果取消任务成功则返回true，
     * 如果取消任务失败则返回false，
     * 如果取消已经完成的任务也会返回false
     * @param mayInterruptIfRunning 是否允许取消正在执行却没有执行完毕的任务
     */
    boolean cancel(boolean mayInterruptIfRunning);

    /**
     * 任务是否被取消成功，如果在任务正常完成前被取消成功，则返回true。
     */
    boolean isCancelled();

    /**
     * 任务是否已经完成，若任务完成，则返回true。
     */
    boolean isDone();

    /**
     * 获取执行结果，这个方法会产生阻塞，会一直等到任务执行完毕才返回。
     */
    V get() throws InterruptedException, ExecutionException;

    /**
     * 获取执行结果，如果在指定时间内，还没获取到结果，就直接返回null。
     */
    V get(long timeout, TimeUnit unit)
        throws InterruptedException, ExecutionException, TimeoutException;
}
```

# FutureTask

因为Future只是一个接口，所以是无法直接用来创建对象使用的，FutureTask是Future接口的一个唯一实现类。

FutureTask实现了RunnableFuture接口。它既可以作为Runnable被线程执行，又可以作为Future得到Callable的返回值。

# 使用Callable+Future获取执行结果

```java
public class Test {
    public static void main(String[] args) {
        ExecutorService executor = Executors.newCachedThreadPool();
        Task task = new Task();
        Future<Integer> result = executor.submit(task);
        executor.shutdown();
         
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e1) {
            e1.printStackTrace();
        }
         
        System.out.println("主线程在执行任务");
         
        try {
            System.out.println("task运行结果"+result.get());
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
         
        System.out.println("所有任务执行完毕");
    }
}
class Task implements Callable<Integer>{
    @Override
    public Integer call() throws Exception {
        System.out.println("子线程在进行计算");
        Thread.sleep(3000);
        int sum = 0;
        for(int i=0;i<100;i++)
            sum += i;
        return sum;
    }
}
```

# 使用Callable+FutureTask获取执行结果

```java
public class Test {
    public static void main(String[] args) {
        //第一种方式
        ExecutorService executor = Executors.newCachedThreadPool();
        Task task = new Task();
        FutureTask<Integer> futureTask = new FutureTask<Integer>(task);
        executor.submit(futureTask);
        executor.shutdown();
         
        //第二种方式，注意这种方式和第一种方式效果是类似的，只不过一个使用的是ExecutorService，一个使用的是Thread
        /*Task task = new Task();
        FutureTask<Integer> futureTask = new FutureTask<Integer>(task);
        Thread thread = new Thread(futureTask);
        thread.start();*/
         
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e1) {
            e1.printStackTrace();
        }
         
        System.out.println("主线程在执行任务");
         
        try {
            System.out.println("task运行结果"+futureTask.get());
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        }
         
        System.out.println("所有任务执行完毕");
    }
}
class Task implements Callable<Integer>{
    @Override
    public Integer call() throws Exception {
        System.out.println("子线程在进行计算");
        Thread.sleep(3000);
        int sum = 0;
        for(int i=0;i<100;i++)
            sum += i;
        return sum;
    }
}
```
