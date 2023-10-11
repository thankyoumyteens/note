# centos7没有ifconfig命令解决办法
```
yum install ifconfig
```
提示没有ifconfig安装包。再使用
```
yum search ifconfig
```
来搜索下ifconfig的相关包

发现ifconfig匹配的是net-tools.x86_64包，安装net-tools.x86_64包
```
yum install net-tools.x86_64 -y
```
完成

另外输入ip addr 也可以查询ip地址
