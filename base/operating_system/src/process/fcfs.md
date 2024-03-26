# 先来先服务算法

先来先服务（First-Come, First-Served, FCFS）算法是一种最简单的进程调度算法。在这种算法中, 进程按照它们到达就绪队列的顺序被调度。第一个到达就绪队列的进程将被第一个调度, 然后是第二个到达的进程, 依此类推。

FCFS 算法适用于不需要交互或响应时间要求不高的批量处理系统。然而, 由于其固有的缺点, 现代操作系统通常不单独使用 FCFS 作为主要的调度算法, 而是结合其他更复杂的调度策略来提高系统的整体性能。

下面是 FCFS 算法的 Java 代码实现:

```java
// 模拟进程类，包含进程ID和到达时间
class Process {
    int pid; // 进程ID
    int arrivalTime; // 进程到达时间

    public Process(int pid, int arrivalTime) {
        this.pid = pid;
        this.arrivalTime = arrivalTime;
    }

    public void printProcess() {
        System.out.println("Process ID: " + pid + ", Arrival Time: " + arrivalTime);
    }
}

// 模拟CPU调度的类
class FCFSScheduler {
    // 用于存储进程的队列，按照到达时间排序
    LinkedList<Process> readyQueue = new LinkedList<>();

    // 添加进程到就绪队列
    public void addProcess(Process process) {
        // 将进程按照到达时间顺序插入到队列中
        // 这里简单地将进程添加到队尾，实际应用中可能需要根据到达时间进行排序
        readyQueue.addLast(process);
    }

    // 执行调度算法
    public void schedule() {
        int totalTime = 0; // 用于记录总的模拟时间
        Process currentProcess = null; // 当前正在执行的进程

        // 当队列不为空时，继续执行
        while (!readyQueue.isEmpty()) {
            currentProcess = readyQueue.poll(); // 取出队列的第一个进程
            System.out.println("Executing Process ID: " + currentProcess.pid);

            // 模拟进程执行时间，这里假设每个进程执行时间为2个时间单位
            for (int i = 0; i < 2; i++) {
                System.out.println("Time: " + (totalTime + i) + ", Process " + currentProcess.pid + " is running.");
                totalTime++; // 时间加一
            }

            // 进程执行完毕
            System.out.println("Process ID: " + currentProcess.pid + " has completed.");
        }
    }
}

// 主函数，用于测试FCFS调度算法
public class FCFSSimulation {
    public static void main(String[] args) {
        FCFSScheduler scheduler = new FCFSScheduler();

        // 添加进程到调度器的就绪队列中
        scheduler.addProcess(new Process(1, 0)); // 进程1，到达时间0
        scheduler.addProcess(new Process(2, 1)); // 进程2，到达时间1
        scheduler.addProcess(new Process(3, 2)); // 进程3，到达时间2

        // 开始执行调度算法
        scheduler.schedule();
    }
}
```

输出:

```
Executing Process ID: 1
Time: 0, Process 1 is running.
Time: 2, Process 1 is running.
Process ID: 1 has completed.
Executing Process ID: 2
Time: 2, Process 2 is running.
Time: 4, Process 2 is running.
Process ID: 2 has completed.
Executing Process ID: 3
Time: 4, Process 3 is running.
Time: 6, Process 3 is running.
Process ID: 3 has completed.
```
