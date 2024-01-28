# 初始化新生代的大小

新生代的大小就是新生代 reion 的个数。在初始化阶段, G1 会确定新生代预期 region 个数的可选范围\[min_young_length, max_young_length\]的计算方法。在后续调整新生代 region 的时候, G1 会先使用初始化时确定的计算方法计算出新生代 region 个数的可选范围, 然后从这个范围中找到一个满足 MaxGCPauseMillis 的最大值。
