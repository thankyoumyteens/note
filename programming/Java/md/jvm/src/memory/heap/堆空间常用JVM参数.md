# 堆空间常用JVM参数

- -XX:+PrintFlagsInitial 查看所有的JVM参数的默认初始值
- -XX:+PrintFlagsFinal 查看所有的JVM参数的最终值
- -Xms 初始堆空间内存(默认为物理内存的1/64)，示例：-Xms100m表示设置为100MB
- -Xmx 最大堆空间内存(默认为物理内存的1/4)，示例：-Xmx100m表示设置为100MB
- -Xmn 设置新生代的大小，通过这个值也可以得到老生代的大小：-Xmx减去-Xmn
- -XX:NewRatio 配置新生代与老年代在堆结构的占比，默认-XX:NewRatio=2，表示新生代占1，老年代占2，新生代占整个堆的1/3
- -XX:SurvivorRatio 设置新生代中Eden和Survivor空间的比例，默认-XX:SurvivorRatio=8，表示Eden，SurvivorFrom，SurvivorTo的比例为8:1:1
- -XX:MaxTenuringThreshold 设置新生代垃圾的最大年龄，默认-XX:MaxTenuringThreshold=15
- -XX:+PrintGCDetaiIs 输出详细的GC处理日志
- -XX:+PrintGC 打印GC简要信息
- -XX:Hand1epromotionFai1ure 是否设置空间分配担保
