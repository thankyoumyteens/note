# 堆空间常用 JVM 参数

- -XX:+PrintFlagsInitial 查看所有的 JVM 参数的默认初始值
- -XX:+PrintFlagsFinal 查看所有的 JVM 参数的最终值
- -Xms 初始堆空间内存(默认为物理内存的 1/64), 示例: -Xms100m 表示设置为 100MB
- -Xmx 最大堆空间内存(默认为物理内存的 1/4), 示例: -Xmx100m 表示设置为 100MB
- -Xmn 设置新生代的大小, 通过这个值也可以得到老生代的大小: -Xmx 减去-Xmn
- -XX:NewRatio 配置新生代与老年代在堆结构的占比, 默认-XX:NewRatio=2, 表示新生代占 1, 老年代占 2, 新生代占整个堆的 1/3
- -XX:SurvivorRatio 设置新生代中 Eden 和 Survivor 空间的比例, 默认-XX:SurvivorRatio=8, 表示 Eden, SurvivorFrom, SurvivorTo 的比例为 8:1:1
- -XX:MaxTenuringThreshold 设置新生代垃圾的最大年龄, 默认-XX:MaxTenuringThreshold=15
- -XX:+PrintGCDetaiIs 输出详细的 GC 处理日志
- -XX:+PrintGC 打印 GC 简要信息
- -XX:Hand1epromotionFai1ure 是否设置空间分配担保
- -XX:+UseTLAB 开启 TLAB, 默认开启
- -XX:PretenureSizeThreshold 指定大于该设置值的对象直接在老年代分配, 只对 Serial 和 ParNew 两款新生代收集器有效
