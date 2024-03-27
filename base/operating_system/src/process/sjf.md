# 短作业优先算法

作业（Job）是指用户提交给系统执行的一个任务单元, 可以是一个程序、一个脚本或者一组命令的集合。作业是早期操作系统中的一个核心概念, 随着个人计算机和现代操作系统的出现, 作业的概念逐渐被进程和线程所取代。在现代操作系统中, 作业管理通常被整合到进程管理中, 每个作业通常对应一个或多个进程。

短作业优先（Shortest Job First, SJF）算法的核心思想是优先执行那些预计执行时间最短的任务, 以此来减少等待时间和提高系统的整体吞吐量。

当一个新任务到达时, 它会进入就绪队列等待调度。调度器会检查就绪队列中的所有任务, 并选择预计执行时间最短的任务来执行。在非抢占式 SJF 中, 一旦任务开始执行, 它会一直运行到完成, 即使有更短的任务到达。而在抢占式 SJF 中, 如果一个新的任务到达, 并且其预计执行时间比当前正在执行的任务还要短, 那么当前任务会被中断, 新任务将获得 CPU。

由于 SJF 算法总是选择执行时间短的任务, 所以它可以减少任务在就绪队列中的等待时间。对于需要快速响应的任务, SJF 算法能够提供较好的服务。通过频繁地完成短任务, 系统可以在单位时间内完成更多的任务。

然而在实际应用中, 很难准确预测一个任务的执行时间, 这使得 SJF 算法在某些情况下可能不如其他算法有效。长作业可能会长时间得不到服务, 因为总有短作业不断地到来并优先执行。

以下是 SJF 算法的 Java 代码实现:

```java
// 模拟进程类, 包含进程ID、到达时间和服务时间（执行时间）
class Process implements Comparable<Process> {
    int pid; // 进程ID
    int arrivalTime; // 到达时间
    int serviceTime; // 服务时间

    // 构造函数
    public Process(int pid, int arrivalTime, int serviceTime) {
        this.pid = pid;
        this.arrivalTime = arrivalTime;
        this.serviceTime = serviceTime;
    }

    // 比较两个进程的服务时间, 用于优先队列的排序
    @Override
    public int compareTo(Process otherProcess) {
        // 如果服务时间短, 则优先级高
        return this.serviceTime - otherProcess.serviceTime;
    }

    // 打印进程信息
    public void printProcess() {
        System.out.println("Process ID: " + pid + ", Arrival Time: " + arrivalTime + ", Service Time: " + serviceTime);
    }
}

// 短作业优先（SJF）调度算法的实现
public class SJFScheduler {
    PriorityQueue<Process> readyQueue; // 使用优先队列存储进程, 按服务时间排序

    // 构造函数, 初始化优先队列
    public SJFScheduler() {
        // 优先队列默认按照自然顺序排序, 这里通过自定义比较规则来按服务时间排序
        readyQueue = new PriorityQueue<>();
    }

    // 添加进程到就绪队列
    public void addProcess(Process process) {
        readyQueue.offer(process); // 将进程添加到优先队列
    }

    // 执行调度算法
    public void schedule() {
        int currentTime = 0; // 当前模拟时间
        int waitingTime = 0; // 等待时间
        int turnaroundTime = 0; // 周转时间

        while (!readyQueue.isEmpty()) {
            Process currentProcess = readyQueue.poll(); // 获取下一个要执行的进程

            // 模拟进程执行
            System.out.println("Executing Process ID: " + currentProcess.pid + ", Service Time: " + currentProcess.serviceTime + " units");
            currentTime += currentProcess.serviceTime; // 更新当前时间
            waitingTime += currentProcess.serviceTime; // 计算等待时间
            turnaroundTime += currentTime - currentProcess.arrivalTime; // 计算周转时间

            // 打印进程执行信息
            System.out.println("Process ID: " + currentProcess.pid + " has completed. Waiting Time: " + waitingTime + " units, Turnaround Time: " + turnaroundTime + " units\n");
        }
    }

    // 主函数, 用于测试SJF调度算法
    public static void main(String[] args) {
        SJFScheduler sjfScheduler = new SJFScheduler();

        // 添加进程到调度器的就绪队列中
        sjfScheduler.addProcess(new Process(1, 0, 7)); // 进程1, 到达时间0, 服务时间7
        sjfScheduler.addProcess(new Process(2, 1, 5)); // 进程2, 到达时间1, 服务时间5
        sjfScheduler.addProcess(new Process(3, 2, 3)); // 进程3, 到达时间2, 服务时间3

        // 开始执行调度算法
        sjfScheduler.schedule();
    }
}
```

输出:

```
Executing Process ID: 3, Service Time: 3 units
Process ID: 3 has completed. Waiting Time: 3 units, Turnaround Time: 1 units

Executing Process ID: 2, Service Time: 5 units
Process ID: 2 has completed. Waiting Time: 8 units, Turnaround Time: 8 units

Executing Process ID: 1, Service Time: 7 units
Process ID: 1 has completed. Waiting Time: 15 units, Turnaround Time: 23 units
```
