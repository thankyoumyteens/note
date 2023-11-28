# 单独使用Mybatis

在mybatis.xml配置文件中添加如下配置: 
```xml
<setting name="logImpl" value="STDOUT_LOGGING" />
```

# 和SpringBoot整合

## 方法1

application.yml
```yaml
#mybatis配置
mybatis:
  # 控制台打印sql日志
  configuration:
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
```

## 方法2

application.yml
```yaml
logging:
  level:
    xx包名: debug
```
