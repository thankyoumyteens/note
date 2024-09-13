# 调优参数

- 设置堆大小: `-Xms` 设置初始大小, 一般是物理内存的 1/64。`-Xmx` 设置最大大小, 一般是物理内存的 1/4
- 设置每个线程栈的大小: `-Xss`
- 设置新生代: `-XX:SurvivorRatio=8` 表示 Eden:S1:S0 = 8:1:1
- 设置晋升老年代的阈值: `-XX:MaxTenuringThreshold=15`
- 设置垃圾回收器: `-XX:+UseG1GC`
