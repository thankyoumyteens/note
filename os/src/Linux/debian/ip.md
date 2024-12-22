# 修改 ip 地址

## 临时修改

```sh
# 查看网络接口信息
ip addr show
# 删除指定网络接口原来的IP地址
sudo ip addr del 原来的IP地址/子网掩码长度 dev 网络接口
# 为指定网络接口添加新的IP地址
# 例子: sudo ip addr add 192.168.43.128/24 dev enp0s1
sudo ip addr del 新的IP地址/子网掩码长度 dev 网络接口
sudo ip link set eth0 up
```
