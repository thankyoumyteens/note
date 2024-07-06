有一个Maven项目, 里面有common模块和主模块, 其中common模块中有若干个mybatis的mapper和xml, 结果主模块调用其mapper时提示出错, 原因是找不到mapper对应的xml映射关系

查资料得知, 主模块的application.yml里面,配置mybatis的mapper-locations时, 用的是classpath, 只会扫描当前moduler的class, 而改为classpath*则会扫描所有jar

```yaml
mybatis:
    mapper-locations: classpath*:mappers/*Mapper.xml
```
