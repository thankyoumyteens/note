# SpringBoot+Maven多模块环境

- 模块AdminWeb：com.adminweb.AdminLoginController.class
- 模块AdminLogin：com.adminlogin.AdminLoginService.class

AdminLoginController中依赖了AdminLoginService

当maven包引入了，使用@Autowired时，未正确扫描时，会提示，该类不能直接依赖注入，编译也会报错

主要是因为在启动AdminWeb模块时，@SpringBootApplication注解会扫描AdminWebApplication当前包及其子包，

这样就扫描不到AdminLogin模块的文件了，需要手动指定扫描包

```java
@SpringBootApplication(scanBasePackages = {"com.adminweb", "com.adminlogin"})
```
