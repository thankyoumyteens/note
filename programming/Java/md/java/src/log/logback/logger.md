# Logger

用来设置某一个包或具体的某一个类的日志打印级别和 Appender, root 节点也是 logger 元素, 是根 logger。

```xml
<configuration>
    <logger name="com.example" level="DEBUG">
        <appender-ref ref="CONSOLE"/>
        <appender-ref ref="FILE"/>
    </logger>

    <root level="INFO">
        <appender-ref ref="CONSOLE"/>
        <appender-ref ref="FILE"/>
    </root>
</configuration>
```

- name: 指定使用这个 logger 的包或类。root 节点的 name 就是 root
- level: 指定日志级别
