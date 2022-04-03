# NAT模式

客户端将访问vip报文发送给LVS服务器

LVS服务器将请求报文的目的地址修改为后端真实服务器，发送给后端真实服务器

后端服务器在处理完之后要将响应的报文返回给LVS

LVS将后端真实服务响应客户端的报文原地址改为自己的ip地址，发送给客户端

# 环境

- LVS：VIP=10.211.102.47 DIP=172.16.100.10
- Nginx1：172.16.100.20
- Nginx2：172.16.100.30

# 负载均衡服务器配置

安装 ipvsadm 并执行相关配置

```
yum install ipvsadm
vim lvs_nat.sh
```
内容如下
```sh
echo 1 > /proc/sys/net/ipv4/ip_forward
vip=10.211.102.47
rs1=172.16.100.20
rs2=172.16.100.30
/sbin/ipvsadm -C
/sbin/ipvsadm -A -t $vip:8088 -s rr
/sbin/ipvsadm -a -t $vip:8088 -r $rs1:8088 -m
/sbin/ipvsadm -a -t $vip:8088 -r $rs2:8088 -m
```
执行脚本
```
/bin/bash lvs_nat.sh
```

查看服务配置信息

```
ipvsadm -ln
```
输出
```
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port Scheduler Flags
-> RemoteAddress:Port Forward Weight ActiveConn InActConn
TCP 10.211.102.47:8088 rr
-> 172.16.100.20:8088 Masq 1 0 0
-> 172.16.100.30:8088 Masq 1 0 0
```

# 后端服务器配置

```
vim rs_nat.sh
```
如下内容
```sh
# 默认网关配置为负载均衡的 DIP
route add default gw 172.16.100.10 dev eth0
```

执行脚本
```
/bin/bash rs_nat.sh
```
