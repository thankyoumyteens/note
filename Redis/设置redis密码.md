# 设置redis密码

需要永久配置密码的话就去redis.conf的配置文件中找到`requirepass`这个参数, 如下配置：

修改redis.conf配置文件
```
# requirepass foobared
requirepass 123
```
保存后重启redis就可以了
