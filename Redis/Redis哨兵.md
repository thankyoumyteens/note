# Redis哨兵

哨兵（Sentinel）是一个独立的进程，作为进程，它会独立运行。哨兵通过发送命令，等待Redis服务器响应，从而监控运行的多个Redis实例

当哨兵监测到master不可用，会自动将slave切换成master，然后通知其他的slave，修改配置文件，让它们切换master。当原来的master恢复后, 会变为slave

# 配置哨兵

redis.conf
```conf
# 禁止保护模式, 使外部网络可以直接访问
protected-mode no
```

sentinel.conf
```conf
# 设置sentinel 的端口
port 26379
# 监控master
# mymaster代表master的别名，可以自定义
# 192.168.11.128代表master的ip
# 6379代表master的端口
# 2代表只有当两个或两个以上的哨兵认为主服务器不可用的时候，才会切换master
sentinel monitor mymaster 192.168.11.128 6379 2
# 配置master的访问密码
# mymaster是master的别名
# 123456是master的密码
sentinel auth-pass mymaster 123456
```

# 启动哨兵

```
redis-sentinel sentinel.conf
```
