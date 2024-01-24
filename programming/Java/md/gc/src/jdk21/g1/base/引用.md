# 引用

Java 中有四种引用类型: 强引用、软引用、弱引用、虚引用。

## 强引用

一般的 Java 对象都是强引用:

```java
Object o = new Object();
```

只要某个对象有强引用与之关联, 这个对象永远不会被回收。

## 软引用

软引用就是把对象用 SoftReference 包裹一下, 如果要从软引用对象获得包裹的对象, 只要 get 一下就可以了:

```java
SoftReference<Object> sr = new SoftReference<Object>(new Object());
Object o = sr.get();
System.out.println(o);
```

当内存不足, 会触发 GC, 如果 GC 后, 内存还是不足, 就会清理软引用(前提是软引用指向的对象没有其它的强引用了)。软引用适合用作缓存, 当内存足够, 可以正常的拿到缓存, 当内存不够, 就会先清理缓存, 不至于马上抛出 OOM。

## 弱引用

```java
WeakReference<Object> wr = new WeakReference<Object>(new Object());
System.out.println(wr.get());
```

弱引用的特点是不管内存是否足够, 只要发生 GC, 都会被回收(前提是弱引用指向的对象没有其它的强引用了)。弱引用在很多地方都有用到, 比如 ThreadLocal、WeakHashMap。

## 虚引用

```java
ReferenceQueue queue = new ReferenceQueue();
PhantomReference<Object> pr = new PhantomReference<Object>(new Object(), queue);
System.out.println(pr.get()); // 输出: null
```

如果一个对象仅持有虚引用, 那么它就和没有任何引用一样, 只要发生 GC, 都会被回收。无法通过虚引用来获取对一个对象的真实引用。虚引用必须和引用队列(ReferenceQueue)联合使用。当垃圾回收器准备回收一个对象时, 如果发现它还有虚引用, 就会在回收对象的内存之前, 把这个虚引用加入到与之关联的引用队列中。可以通过引用队列检测对象是否已经从内存中删除。
