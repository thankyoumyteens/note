# ThreadLocal

使用 ThreadLocal 可以为每个使用该变量的线程提供一个独立的变量副本, 各个线程间的数据互不干扰。

```java
private static ThreadLocal<Integer> threadLocal = new ThreadLocal<>();

public static void main(String[] args) {
    // 设置值
    threadLocal.set(1);

    // 获取值
    Integer value = threadLocal.get();

    // 移除值
    threadLocal.remove();
}
```

## 原理

ThreadLocal 的实现原理主要依赖于 Java 内部的 Thread 类和 ThreadLocalMap 类。ThreadLocalMap 的键是 ThreadLocal 对象, 值是线程局部变量的值。ThreadLocalMap 使用 ThreadLocal 对象的弱引用作为键, 这样可以在 ThreadLocal 被垃圾回收时自动清理键值对。

### set 的步骤

1. 获取当前线程对象 Thread currentThread
2. 从 currentThread 获取 ThreadLocalMap
3. 如果 ThreadLocalMap 为空, 则创建一个新的 ThreadLocalMap
4. 将当前 ThreadLocal 对象作为键, 值作为值, 存储到 ThreadLocalMap 中

```java
public void set(T value) {
    set(Thread.currentThread(), value);
}

private void set(Thread t, T value) {
    ThreadLocalMap map = getMap(t);
    if (map != null) {
        map.set(this, value);
    } else {
        createMap(t, value);
    }
}
```

### get 的步骤

1. 获取当前线程对象 Thread currentThread
2. 从 currentThread 获取 ThreadLocalMap
3. 从 ThreadLocalMap 中获取与当前 ThreadLocal 对象关联的值

```java
public T get() {
    return get(Thread.currentThread());
}
private T get(Thread t) {
    ThreadLocalMap map = getMap(t);
    if (map != null) {
        ThreadLocalMap.Entry e = map.getEntry(this);
        if (e != null) {
            @SuppressWarnings("unchecked")
            T result = (T) e.value;
            return result;
        }
    }
    return setInitialValue(t);
}
```

## remove 的步骤

1. 获取当前线程对象 Thread currentThread
2. 从 currentThread 获取 ThreadLocalMap
3. 从 ThreadLocalMap 中移除与当前 ThreadLocal 对象关联的键值对

```java
public void remove() {
    remove(Thread.currentThread());
}
private void remove(Thread t) {
    ThreadLocalMap m = getMap(t);
    if (m != null) {
        m.remove(this);
    }
}
```

## 内存泄露的问题

假如 ThreadLocalMap 的 key 和被回收之后, entry 中就存在 key 为 null, 但是 value 有值的 entry 对象, 但是永远没办法被访问到, 同样除非线程结束运行。

但是只要在使用完之后及时调用 remove 方法删除 Entry 对象, 实际上是不会出现这个问题的。
