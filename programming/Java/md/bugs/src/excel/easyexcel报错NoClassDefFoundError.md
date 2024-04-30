# easyexcel 报错 NoClassDefFoundError

```java
public static Class<?> generateExportClass(String prototypeName) {
    // ASM生成导出类VO(略)
    // 使用自定义classloader加载并返回
    return classLoader.load(targetName, writer.toByteArray());
}

// 自定义classloader
public class ExcelExportClassLoader extends ClassLoader {
    public Class<?> load(String fullClassName, byte[] b) {
        return defineClass(fullClassName, b, 0, b.length);
    }
}
```

导出时报错:

```
com.alibaba.easyexcel.support.cglib.core.CodeGenerationException: java.lang.NoClassDefFoundError-->com/alibaba/easyexcel/support/cglib/beans/BeanMap
        at com.alibaba.easyexcel.support.cglib.core.ReflectUtils.defineClass(ReflectUtils.java:558)
        at com.alibaba.easyexcel.support.cglib.core.AbstractClassGenerator.generate(AbstractClassGenerator.java:363)
        at com.alibaba.easyexcel.support.cglib.core.AbstractClassGenerator$ClassLoaderData$3.apply(AbstractClassGenerator.java:110)
        at com.alibaba.easyexcel.support.cglib.core.AbstractClassGenerator$ClassLoaderData$3.apply(AbstractClassGenerator.java:108)
        at com.alibaba.easyexcel.support.cglib.core.internal.LoadingCache$2.call(LoadingCache.java:54)
        at java.util.concurrent.FutureTask.run(FutureTask.java:266)
        at com.alibaba.easyexcel.support.cglib.core.internal.LoadingCache.createEntry(LoadingCache.java:61)
        ...
```

原因是使用了自定义类加载器, 默认情况下，类加载器之间不是相互可见的。也就是说，一个类加载器加载的类对于另一个类加载器来说是不可见的，除非它们存在父子关系（即一个加载器是另一个加载器的父加载器）。

## 解决

使用默认的类加载器加载:

```java
public static Class<?> generateExportClass(String prototypeName) {
    // ASM生成导出类VO(略)
    // 把新生成的类写入文件
    writeToFile(klassName, writer.toByteArray());
    // 使用自默认的classloader加载并返回
    return Class.forName(klassName);
}
```
