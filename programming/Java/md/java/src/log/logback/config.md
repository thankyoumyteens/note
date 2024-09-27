# 配置文件

logback 查找配置文件的顺序:

1. 查找系统环境变量 `logback.configurationFile` 指定的配置文件, 例如通过启动命令设置: `java -Dlogback.configurationFile=123.xml demo.jar`
2. 查找 classpath 下(放到 idea 的 resource 目录下)的 logback-test.xml 文件
3. 查找 classpath 下的 logback.xml 文件
4. 如果都没有, 则默认输出到控制台

## configuration

根节点

```xml
<configuration scan="true" scanPeriod="1000" debug="false">
</configuration>
```

- scan: 配置文件修改后是否重新加载。默认 true
- scanPeriod: 检查配置文件是否修改的时间间隔。默认单位是毫秒。默认值 1 分钟
- debug: 是否打印 logback 内部日志。默认值 false
