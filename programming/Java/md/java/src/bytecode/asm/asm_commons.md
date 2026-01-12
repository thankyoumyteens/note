# asm-commons

核心包是 org.objectweb.asm.commons，它不是必须的，但：

- 提供了大量 封装好的 Visitor / 工具方法
- 避免你自己去算局部变量 slot、栈深、方法描述符这些细节
- 很适合写 AOP / 监控 / 日志 / 统计这类字节码增强
