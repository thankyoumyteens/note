# try中有return时finally还会执行吗

try中有return, 会先将值暂存，无论finally语句中对该值做什么处理，最终返回的都是try语句中的暂存值。当try与finally语句中均有return语句，会忽略try中return。

# RabbitMQ六种消息模型

# 消息可靠性投递

# RabbitMQ集群架构模式

# RabbitMQ幂等性

# Redis缓存穿透缓存击穿缓存雪崩

# Redis持久化 AOF RDB

# # Redis哨兵

# Redis数据类型

# Redis缓存过期处理与内存淘汰机制

# Spring中的事务传播行为

# 接口幂等性

#  == 和 equals 的区别是什么

== 对基本类型是值比较，对引用类型是引用比较。equals 默认情况下是引用比较，只是 String、Integer 等类重写了 equals 方法，把它变成了值比较，所以一般情况下 equals 比较的是值是否相等。

# Math.round(-1.5) 等于多少

等于-1，因为在数轴上取值时是向右取整

# StringBuffer 和 StringBuilder 区别

StringBuffer 是线程安全的，而 StringBuilder 是非线程安全的，但 StringBuilder 的性能却高于 StringBuffer（因为stringbuffer加锁了），所以在单线程环境下推荐使用 StringBuilder，多线程环境下推荐使用 StringBuffer。

# String str="i"与 String str=new String("i")一样吗

不一样，因为内存的分配方式不一样。String str="i"的方式，Java 虚拟机会将其分配到常量池中（常量池保存在方法区中）；而 String str=new String("i") 则会被分到堆内存中。

# 如何将字符串反转？

使用 StringBuilder 或者 stringBuffer 的 reverse() 方法。

或者对撞指针
```java
void reverseString(char[] s) {
    int l = 0;
    int r = s.length - 1;
    while (l < r) {
        swap(s, l++, r--);
    }
}
void swap(char[] arr, int i, int j){
    char t = arr[i];
    arr[i] = arr[j];
    arr[j] = t;
}
```

