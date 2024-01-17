# 基本用法

配置依赖:

```xml
<!-- https://mvnrepository.com/artifact/org.javassist/javassist -->
<dependency>
    <groupId>org.javassist</groupId>
    <artifactId>javassist</artifactId>
    <version>3.30.2-GA</version>
</dependency>
```

使用:

```java
public class JavassistDemo {

    public static void main(String[] args) {
        try {
            ClassPool pool = ClassPool.getDefault();
            // 创建Person类
            CtClass classPerson = pool.makeClass("com.demo.Person");
            // 生成.class文件
            // 文件路径: C:\Users\Public\com\demo\Person.class
            classPerson.writeFile("C:\\Users\\Public");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```
