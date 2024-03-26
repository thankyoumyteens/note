# 高响应比优先算法

高响应比优先算法（Highest Response Ratio Next, HRRN）算法为每个进程计算一个响应比，具有最高响应比的进程将被调度执行。

响应比的计算公式如下：

```
响应比 = (等待时间 + 服务时间) / 服务时间
```

当进程进入系统时，它的响应比被初始化为 1。每当一个进程完成执行或者有新的进程到达时，系统重新计算所有就绪进程的响应比。系统选择响应比最高的进程来执行。当一个进程开始执行时，它的服务时间开始减少，等待时间增加。当进程执行完毕时，它的服务时间变为 0。为了确保长作业不会被无限期地推迟，HRRN 算法会定期检查并调整响应比，以避免长作业的响应比变得过低。

通过考虑等待时间，HRRN 能够减少短作业的等待时间。通过定期更新响应比，长作业最终会得到执行的机会，避免了饥饿现象。

与先来先服务（FCFS）等简单算法相比，HRRN 需要更频繁地计算响应比，会增加系统的开销。

以下是高响应比优先（HRRN）算法的一个简化的 Java 代码实现。这个实现使用了一个优先队列（`PriorityQueue`），其中每个进程都有一个响应比，并且根据这个响应比进行排序。请注意，这是一个非抢占式的调度算法实现。

```java
// 定义进程类
class Process {
    int pid; // 进程ID
    int arrivalTime; // 到达时间
    int serviceTime; // 服务时间
    int waitingTime; // 等待时间，初始化为0

    // 构造函数
    public Process(int pid, int arrivalTime, int serviceTime) {
        this.pid = pid;
        this.arrivalTime = arrivalTime;
        this.serviceTime = serviceTime;
        this.waitingTime = 0; // 初始化等待时间
    }

    // 更新等待时间
    public void updateWaitingTime(int currentTime) {
        waitingTime = currentTime - arrivalTime;
    }

    // 计算响应比
    public double calculateResponseRatio() {
        return (double) (waitingTime + serviceTime) / serviceTime;
    }

    // 打印进程信息
    public void printProcess() {
        System.out.println("Process ID: " + pid + ", Arrival Time: " + arrivalTime +
                           ", Service Time: " + serviceTime + ", Waiting Time: " + waitingTime);
    }
}

// 定义比较器，用于优先队列中的排序
class ProcessComparator implements Comparator<Process> {
    @Override
    public int compare(Process p1, Process p2) {
        // 降序排序，响应比高的进程优先级高
        return Double.compare(p2.calculateResponseRatio(), p1.calculateResponseRatio());
    }
}

// 高响应比优先调度算法实现
public class HRRNScheduler {
    PriorityQueue<Process> readyQueue; // 就绪队列

    // 构造函数，初始化优先队列
    public HRRNScheduler() {
        readyQueue = new PriorityQueue<>(new ProcessComparator());
    }

    // 添加进程到就绪队列
    public void addProcess(Process process) {
        readyQueue.add(process);
    }

    // 执行调度算法
    public void schedule(int currentTime, int totalTime) {
        while (!readyQueue.isEmpty()) {
            Process currentProcess = readyQueue.poll(); // 获取当前响应比最高的进程
            currentProcess.updateWaitingTime(currentTime); // 更新等待时间

            // 模拟进程执行
            System.out.println("Executing Process: " + currentProcess.pid);
            currentTime += currentProcess.serviceTime; // 更新当前时间

            // 完成进程
            System.out.println("Process " + currentProcess.pid + " completed. Total Time: " + currentTime);
            currentProcess.printProcess(); // 打印进程信息

            // 检查是否所达到总时间
            if (currentTime >= totalTime) {
                break;
            }
        }
    }

    // 主函数，用于测试HRRN调度算法
    public static void main(String[] args) {
        HRRNScheduler scheduler = new HRRNScheduler();

        // 添加进程到调度器的就绪队列中
        scheduler.addProcess(new Process(1, 0, 7)); // 进程1，到达时间0，服务时间7
        scheduler.addProcess(new Process(2, 1, 5)); // 进程2，到达时间1，服务时间5
        scheduler.addProcess(new Process(3, 2, 3)); // 进程3，到达时间2，服务时间3

        // 假设总时间为10个时间单位
        int totalTime = 10;
        scheduler.schedule(0, totalTime); // 开始执行调度算法
    }
}
```

输出:

```
Executing Process: 1
Process 1 completed. Total Time: 7
Process ID: 1, Arrival Time: 0, Service Time: 7, Waiting Time: 0
Executing Process: 3
Process 3 completed. Total Time: 10
Process ID: 3, Arrival Time: 2, Service Time: 3, Waiting Time: 5
```
