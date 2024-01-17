# ClassPool

CtClass 在 Javassist 中表示一个 class 文件。ClassPool 是一个存储 CtClass 的哈希表。ClassPool 会在内存中维护所有被它创建过的 CtClass, 当 CtClass 数量过多时, 会占用大量的内存, 当不再使用某个 CtClass 时, 需要手动调用 CtClass 的 detach() 方法以释放内存。

常用方法:

1. getDefault: 返回默认的 ClassPool, 一般会通过该方法创建 ClassPool
2. appendClassPath: 添加一个 classpath 到类搜索路径的末尾
3. insertClassPath: 添加一个 classpath 到类搜索路径的起始
4. toClass: 把 CtClass 加载到 JVM 中
5. get: 根据类名返回一个 CtClass

## getDefault

```java
/**
 * 返回默认的ClassPool, 一般会通过该方法创建ClassPool
 */
public static synchronized ClassPool getDefault();
```

## appendClassPath

```java
/**
 * 添加一个classpath到类搜索路径的末尾
 *
 * @param cp classpath
 * @return 添加的classpath
 */
public ClassPath appendClassPath(ClassPath cp);

/**
 * 添加一个classpath到类搜索路径的末尾
 *
 * @param pathname 文件夹或者jar包的路径
 * @return 添加的classpath
 * @throws NotFoundException jar包不存在
 */
public ClassPath appendClassPath(String pathname);
```

## insertClassPath

```java
/**
 * 添加一个classpath到类搜索路径的起始
 *
 * @param cp classpath
 * @return 添加的classpath
 */
public ClassPath insertClassPath(ClassPath cp);

/**
 * 添加一个classpath到类搜索路径的起始
 *
 * @param pathname 文件夹或者jar包的路径
 * @return 添加的classpath
 * @throws NotFoundException jar包不存在
 */
public ClassPath insertClassPath(String pathname);
```

## toClass

```java
/**
 * 使用当前线程的类加载器加载类
 * 把CtClass转成java.lang.Class对象
 * 调用这个方法后, CtClass不能再被修改
 * 当前线程的类加载器通过Thread.currentThread().getContextClassLoader()获取
 * JDK 11及后续版本不推荐使用
 *
 * @param clazz 要加载的类
 * @return 完成加载的类
 */
public Class toClass(CtClass clazz);

/**
 * 加载类
 * 把CtClass转成java.lang.Class对象
 * 调用这个方法后, CtClass不能再被修改
 *
 * JDK 9及后续版本可以使用
 *
 * @param ct 要加载的类
 * @param neighbor 相同包下的任意一个已经加载的class对象
 * @return 完成加载的类
 */
public Class<?> toClass(CtClass ct, Class<?> neighbor);
```

## get

```java
/**
 * 根据类名返回一个CtClass
 * 内部类使用$隔开, 比如: com.example.Demo$SubDemo
 *
 * @param classname 类的全限定名
 */
public CtClass get(String classname);
```
