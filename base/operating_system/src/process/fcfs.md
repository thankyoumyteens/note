# 先来先服务算法

先来先服务（First-Come, First-Served, FCFS）算法是一种最简单的进程调度算法。在这种算法中, 进程按照它们到达就绪队列的顺序被调度。第一个到达就绪队列的进程将被第一个调度, 然后是第二个到达的进程, 依此类推。

FCFS 算法适用于不需要交互或响应时间要求不高的批量处理系统。然而, 由于其固有的缺点, 现代操作系统通常不单独使用 FCFS 作为主要的调度算法, 而是结合其他更复杂的调度策略来提高系统的整体性能。

下面是使用 Java 代码来描述先来先服务（FCFS）算法的实现: 

```java
class Process {
    int processId;
    int arrivalTime;
    int burstTime;
    public Process(int processId, int arrivalTime, int burstTime) {
        this.processId = processId;
        this.arrivalTime = arrivalTime;
        this.burstTime = burstTime;
    }
    public void execute() {
        // 模拟进程执行, 这里可以是实际的处理逻辑
        // 假设sleep方法可以模拟进程执行的时间
        try {
            Thread.sleep(burstTime);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("Process " + processId + " has completed.");
    }
}

class FCFScheduler {
    private Queue<Process> readyQueue;
    public FCFScheduler() {
        readyQueue = new LinkedList<>();
    }
    public void addProcess(Process process) {
        readyQueue.add(process);
    }
    public void schedule() {
        while (!readyQueue.isEmpty()) {
            Process currentProcess = readyQueue.poll();
            currentProcess.execute();
        }
    }
}
public class FCFSDemo {
    public static void main(String[] args) {
        FCFScheduler scheduler = new FCFScheduler();
        // 添加一些进程到调度器
        scheduler.addProcess(new Process(1, 0, 5));
        scheduler.addProcess(new Process(2, 1, 3));
        scheduler.addProcess(new Process(3, 2, 8));
        // 开始调度进程
        scheduler.schedule();
    }
}
```
