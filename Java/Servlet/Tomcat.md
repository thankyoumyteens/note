# 修改自身的端口号
conf/server.xml
```xml
<Connector port="8888"
  protocol="HTTP/1.1"
  connectionTimeout="20000"
  redirectPort="8445"/>
```

# 部署项目
## 直接将项目放到webapps目录下即可
## 配置conf/server.xml文件
```xml
<!-- 在<Host>标签中配置 -->
<!-- docBase:项目存放的路径 -->
<!-- path：虚拟目录 -->
<!-- 访问:http://ip/hehe/index.html -->
<Context docBase="D:\hello" path="/hehe" />
```
## 在conf/Catalina/localhost创建任意名称的xml文件。在文件中编写
```xml
<!-- 访问:http://ip/xml文件名/index.html -->
<Context docBase="D:\hello" />
```
