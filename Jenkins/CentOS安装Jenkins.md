# CentOS安装Jenkins
安装
```
sudo wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
yum install jenkins -y
```
启动
```
systemctl start jenkins
```

# 启动jenkins服务错误1
错误信息: Job for jenkins.service failed because the control process exited with error code. See "systemctl status jenkins.service" and "journalctl -xe" for details.

查看错误详情: 
```
systemctl status jenkins.service
```
输出中包含: Starting Jenkins bash: /usr/bin/java: No such file or directory

这个问题比较好解决，因为没有配置好jdk导致的，重新安装jdk，配置好环境变量就行

# 启动jenkins服务错误2
错误信息: Job for jenkins.service failed because the control process exited with error code. See "systemctl status jenkins.service" and "journalctl -xe" for details.

查看错误详情: 
```
systemctl status jenkins.service
```
输出中包含: starting jenkins bash /usr/bin/java permission denied

权限问题, 添加权限
```
chmod a+x /usr/bin/java
```
注意: 有文件权限了，但不一定有文件夹权限

# 启动jenkins服务错误3
```
less /var/log/jenkins/jenkins.log
```
日志中包含: 
```
java.lang.NullPointerException
        at sun.awt.FontConfiguration.getVersion(FontConfiguration.java:1264)
```

原因是OpenJDK中没有相关的API

执行下面的命令再重新启动就行了
```
yum install fontconfig -y
```

# Jenkins修改显示语言为英文
Manage Jenkins -> Configure System -> Locale
- 若修改为中文简体，Default Language设置为：zh_cn
- 若修改为中文繁体，Default Language设置为：zh_tw
- 若要修改回英文，Default Language设置为：en_us

勾选："Ignore browser preference and force this language to all users" 并保存。

浏览器地址栏输入 http://localhost:8080/restart 重启jenkins

# 关闭和重启Jenkins

### 关闭Jenkins
在访问jenkins服务器的网址url地址后加上exit。

例如我jenkins的地址http://localhost:8080/，那么我只需要在浏览器地址栏上敲下http://localhost:8080/exit，就能关闭jenkins服务

### 重启Jenkies
http://localhost:8080/restart

### 重新加载配置信息
http://localhost:8080/reload

