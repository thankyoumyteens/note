# 配置文件

logback 查找配置文件的顺序:

1. 查找系统环境变量 `logback.configurationFile` 指定的配置文件, 例如通过启动命令设置: `java -Dlogback.configurationFile=123.xml demo.jar`
2. 查找 classpath 下(放到 idea 的 resource 目录下)的 logback-test.xml 文件
3. 查找 classpath 下的 logback.xml 文件
4. 如果都没有, 则默认输出到控制台
