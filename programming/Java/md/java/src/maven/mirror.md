# 设置国内源

修改 conf/settings.xml 文件:

```xml
<mirrors>
  <mirror>
    <id>aliyunmaven</id>
    <mirrorOf>*</mirrorOf>
    <name>阿里云公共仓库</name>
    <url>https://maven.aliyun.com/repository/public</url>
  </mirror>
  <mirror>
    <id>huaweicloud</id>
    <mirrorOf>central</mirrorOf>
    <url>https://mirrors.huaweicloud.com/repository/maven/</url>
  </mirror>
</mirrors>
```
