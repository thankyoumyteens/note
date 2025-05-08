# Process finished with exit code 1

启动项目后显示 Process finished with exit code 1 直接停了, 也不报错。

## 解决

把 SpringApplication.run 用 try-catch 包起来

```java
public static void main(String[] args) {
    try {
        SpringApplication.run(MyApplication.class, args);
    } catch (Exception e) {
        // 输出异常
        e.printStackTrace();
    }
}
```
