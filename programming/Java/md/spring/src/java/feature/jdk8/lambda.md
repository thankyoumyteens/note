# lambda 表达式

lambda 表达式可以替换只有单个抽象方法的接口。

原始的匿名内部类:

```java
new Thread(new Runnable() {
    @Override
    public void run() {
        System.out.println("new thread");
    }
}).start();
```

使用 lambda 表达式替代:

```java
new Thread(() -> System.out.println("new thread")).start();
```

## 方法引用

方法引用是 lambda 表达式的一种快捷写法。如果 lambda 表达式中的内容就是简单的调用一个已存在的方法, 那么可以使用方法引用替代。

使用 lambda 表达式:

```java
List<String> collect = strList.stream().map((str) -> str.toUpperCase()).collect(Collectors.toList());
```

替换成方法引用:

```java
List<String> collect = strList.stream().map(String::toUpperCase).collect(Collectors.toList());
```
