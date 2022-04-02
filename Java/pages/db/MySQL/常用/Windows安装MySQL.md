# Windows安装MySQL

下载zip包, 解压
···
https://cdn.mysql.com//Downloads/MySQL-5.7/mysql-5.7.34-winx64.zip
···
管理员身份运行cmd
```
cd C:\Users\ILove\Walter\software\mysql-5.7.34-winx64\bin
mysqld -install
mysqld --initialize --console
```
在输出的最后一行是生成的临时密码

即可以在服务管理器中看到MySQL服务, 关闭自动启动

开启mysql的服务
```
net start mysql
```
登录
```
mysql -uroot -p
```
修改密码
```
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('123456');
```

# 卸载

关闭服务
```
net stop mysql
```
删除mysql服务
```
sc delete mysql
```
