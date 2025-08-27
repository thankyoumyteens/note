# 实现受限的导出

修改 user.gui 的模块描述符:

```java
module user.gui {
    requires data.masking;
    // 增加一行
    // 表示com.example.ui包只给data.masking模块访问, 其它模块不能访问
    exports com.example.ui to data.masking;
}
```

重新编译 user.gui 模块后运行, 得到了正确的输出:

```
User{username='admin', password='123456', phone='13800000000', email='admin@example.com'}
User{username='ad****n', password='12****56', phone='13****0000000', email='ad****n@example.com'}
```
