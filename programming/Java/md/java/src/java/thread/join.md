# join 方法

join 方法是 Thread 类的一个实例方法, 它使得调用 join 方法的线程(称为主线程)等待当前执行的线程完成执行后, 主线程才继续执行。

join 方法常用于确保某些操作在其他线程执行之前完成, 例如初始化操作或者确保主线程等待后台线程处理数据后再继续。

```java
public class Tester {

    public static void main(String[] args) {
        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 20; i++) {
                System.out.println("Thread 1: " + i);
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });
        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 20; i++) {
                System.out.println("Thread 2: " + i);
                if (i == 10) {
                    try {
                        // 本线程阻塞
                        // 等待t1执行结束才会继续执行
                        t1.join();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });

        t1.start();
        t2.start();
    }
}
```
