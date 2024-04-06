# Peterson 算法

Peterson 算法是一种经典的软件解决方案, 用于实现两个进程之间的互斥。这个算法由 Gary L. Peterson 在 1981 年提出, 它是一种使用两个进程的合作来实现互斥的方法, 不需要使用硬件支持的同步原语, 如互斥锁。

它结合双标志法、单标志法的思想。两个进程不再争着进入临界区, 而是优先让对方进入临界区。

### 算法描述

Peterson 算法基于两个进程, P0 和 P1, 它们共享一个资源, 并且都想进入临界区。每个进程都有自己的私有变量`flag`和一个公共变量`turn`。`flag`用于指示进程是否想要进入临界区, 而`turn`用于指示轮到哪个进程进入临界区。

算法步骤如下: 

1. **设置标志**: 每个进程将自己的`flag`设置为真(表示想要进入临界区), 并将`turn`设置为另一个进程

2. **请求进入**: 每个进程检查另一个进程的`flag`和`turn`。如果`turn`不是自己, 且另一个进程的`flag`为真, 那么进程继续执行循环, 等待另一个进程完成

3. **进入临界区**: 当`turn`是自己, 或者另一个进程的`flag`为假时, 进程可以进入临界区

4. **离开临界区**: 进程完成临界区操作后, 将自己的`flag`设置为假, 这样另一个进程就可以进入临界区了

Peterson 算法用软件方法解决了进程互斥问题, 遵循了空闲让进、忙则等待、有限等待 三个原则, 但是依然未遵循让权等待的原则。

Peterson 算法的 java 代码实现:

```java
public class PetersonAlgorithm {
    private boolean flag[] = new boolean[2]; // 每个进程有一个标志位
    private int turn; // 表示当前允许哪个进程进入临界区

    public void criticalSection(int processId) {
        // 每个进程尝试进入临界区
        flag[processId] = true;
        // 两个进程都先让对方进入临界区
        // 所以后执行到这里的进程会先进入临界区
        turn = 1 - processId; // 设置轮到另一个进程

        // 自旋等待, 直到获得进入临界区的许可
        while (flag[1 - processId] && turn == processId) {
            // 忙等待, 这里可以做一些简单的休眠来减少CPU占用
            try {
                Thread.sleep(1);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        // 临界区代码, 只允许一个进程执行
        System.out.println("Process " + processId + " is in the critical section.");

        // 离开临界区
        flag[processId] = false;
    }

    // 模拟两个进程/线程的运行
    public static void main(String[] args) {
        final int N = 5; // 模拟进程/线程执行的次数
        PetersonAlgorithm peterson = new PetersonAlgorithm();

        // 线程1
        new Thread(() -> {
            for (int i = 0; i < N; i++) {
                peterson.criticalSection(0);
            }
        }).start();

        // 线程2
        new Thread(() -> {
            for (int i = 0; i < N; i++) {
                peterson.criticalSection(1);
            }
        }).start();
    }
}
```
