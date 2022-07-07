java环境搭建

下载jenkins
```
wget https://mirrors.tuna.tsinghua.edu.cn/jenkins/war-stable/2.346.1/jenkins.war
```

安装字体
```
sudo apt install fontconfig -y
```

启动
```
nohup java -jar jenkins.war --httpPort=8080 > jenkins-start.log &
```

查看启动日志, 找到初始密码
```
cat jenkins-start.log
```
