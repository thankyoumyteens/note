# 内存泄漏排查

1. 获取快照 dump
   - 运行时导出 `jmap -dump:[live],format=b,file=<file-path> <pid>`
   - 宕机时自动导出 `java -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=<file-or-dir-path>`
2. VisualVM 分析 dump
3. 查看堆信息，定位问题
